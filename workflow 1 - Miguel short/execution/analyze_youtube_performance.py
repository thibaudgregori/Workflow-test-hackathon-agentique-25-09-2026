"""
Analyze YouTube Performance

Comprehensive YouTube channel analysis combining:
- Current metrics sync to Notion
- Historical time-series analytics
- Traffic source analysis
- AI-powered pattern recognition and recommendations

Tool references:
- tools/youtube.md (YouTube Data API, Analytics API, OAuth)
- tools/notion.md (Notion API patterns)

Directive: directives/analyze_youtube_performance.md
"""

import os
import csv
import json
import argparse
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Configuration
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_CHANNEL_ID = os.getenv("YOUTUBE_CHANNEL_ID")
YOUTUBE_UPLOADS_PLAYLIST_ID = os.getenv("YOUTUBE_UPLOADS_PLAYLIST_ID")
YOUTUBE_BASE_URL = "https://www.googleapis.com/youtube/v3"

# Notion configuration
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
YOUTUBE_NOTION_DB_ID = os.getenv("YOUTUBE_NOTION_DB_ID")
NOTION_BASE_URL = "https://api.notion.com/v1"
NOTION_HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

# Paths
def find_workspace_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / '.env').exists() and (candidate / 'secrets').is_dir():
            return candidate
    raise RuntimeError('Could not find workspace root with .env and secrets/')


WORKSPACE = find_workspace_root()
TOKEN_FILE = WORKSPACE / 'secrets' / 'youtube_oauth_token.json'

# Services (lazy init)
_analytics_services = threading.local()
_youtube_service = None
_youtube_oauth_available = None


def get_youtube_service():
    """Get YouTube Data API v3 service using OAuth. Required for unlisted/private videos."""
    global _youtube_service, _youtube_oauth_available

    if _youtube_oauth_available is False:
        return None
    if _youtube_service is not None:
        return _youtube_service
    if not TOKEN_FILE.exists():
        _youtube_oauth_available = False
        return None

    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        SCOPES = [
            'https://www.googleapis.com/auth/youtube',
            'https://www.googleapis.com/auth/yt-analytics.readonly',
        ]
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        _youtube_service = build('youtube', 'v3', credentials=creds)
        _youtube_oauth_available = True
        return _youtube_service

    except Exception as e:
        print(f"   ⚠️  Could not initialize YouTube Data API with OAuth: {e}")
        _youtube_oauth_available = False
        return None


def get_analytics_service():
    """Get a thread-local YouTube Analytics service using OAuth credentials."""
    if getattr(_analytics_services, 'service', None) is not None:
        return _analytics_services.service

    if not TOKEN_FILE.exists():
        print("   ⚠️  OAuth token not found - analytics features disabled")
        print(f"      Run 'python execution/youtube_oauth_setup.py' to authenticate")
        return None

    try:
        from google.oauth2.credentials import Credentials
        from google.auth.transport.requests import Request
        from googleapiclient.discovery import build

        SCOPES = [
            'https://www.googleapis.com/auth/youtube',
            'https://www.googleapis.com/auth/yt-analytics.readonly',
        ]

        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())

        _analytics_services.service = build('youtubeAnalytics', 'v2', credentials=creds)
        return _analytics_services.service

    except Exception as e:
        print(f"   ⚠️  Could not initialize Analytics API: {e}")
        return None


# ============================================================================
# PHASE 1: Data Collection
# ============================================================================

def fetch_youtube_videos():
    """Fetch all videos from YouTube channel using uploads playlist.
    Uses OAuth when available to include unlisted/private videos.
    Falls back to API key (public only) if OAuth unavailable.
    """
    youtube = get_youtube_service()
    use_oauth = youtube is not None

    if use_oauth:
        print("   (Using OAuth - includes unlisted videos)")
    else:
        print("   (Using API key - public videos only)")

    videos = []
    next_page_token = None

    while True:
        if use_oauth:
            request = youtube.playlistItems().list(
                part='snippet,contentDetails',
                playlistId=YOUTUBE_UPLOADS_PLAYLIST_ID,
                maxResults=50,
                pageToken=next_page_token
            )
            data = request.execute()
        else:
            params = {
                'part': 'snippet,contentDetails',
                'playlistId': YOUTUBE_UPLOADS_PLAYLIST_ID,
                'maxResults': 50,
                'key': YOUTUBE_API_KEY
            }
            if next_page_token:
                params['pageToken'] = next_page_token
            resp = requests.get(f"{YOUTUBE_BASE_URL}/playlistItems", params=params)
            data = resp.json()

        if 'error' in data:
            print(f"❌ YouTube API error: {data['error'].get('message', 'Unknown')}")
            break

        items = data.get('items', [])
        if not items:
            break

        video_ids = [item['contentDetails']['videoId'] for item in items]

        if use_oauth:
            stats_data = youtube.videos().list(
                part='snippet,statistics,contentDetails,status',
                id=','.join(video_ids)
            ).execute()
            videos.extend(stats_data.get('items', []))
        else:
            stats_params = {
                'part': 'snippet,statistics,contentDetails',
                'id': ','.join(video_ids),
                'key': YOUTUBE_API_KEY
            }
            stats_resp = requests.get(f"{YOUTUBE_BASE_URL}/videos", params=stats_params)
            videos.extend(stats_resp.json().get('items', []))

        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break

    return videos


def fetch_video_analytics(video_id: str, start_date: str, end_date: str) -> dict:
    """Fetch aggregate analytics for a specific video."""
    analytics = get_analytics_service()
    if not analytics:
        return {}

    try:
        response = analytics.reports().query(
            ids=f'channel=={YOUTUBE_CHANNEL_ID}',
            startDate=start_date,
            endDate=end_date,
            metrics='estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares',
            filters=f'video=={video_id}'
        ).execute()

        if response.get('rows') and len(response['rows']) > 0:
            row = response['rows'][0]
            return {
                'watch_time_minutes': round(row[0], 1),
                'avg_view_duration_seconds': round(row[1], 1),
                'avg_view_percentage': round(row[2], 2),
                'subscribers_gained': int(row[3]),
                'subscribers_lost': int(row[4]),
                'likes': int(row[5]),
                'comments': int(row[6]),
                'shares': int(row[7])
            }
    except Exception:
        pass
    return {}


# ============================================================================
# PHASE 2: Historical Analytics
# ============================================================================

def fetch_daily_analytics(video_id: str, start_date: str, end_date: str) -> list:
    """Fetch daily time-series analytics for a video."""
    analytics = get_analytics_service()
    if not analytics:
        return []

    try:
        response = analytics.reports().query(
            ids=f'channel=={YOUTUBE_CHANNEL_ID}',
            startDate=start_date,
            endDate=end_date,
            dimensions='day',
            metrics='views,estimatedMinutesWatched,averageViewDuration,averageViewPercentage,subscribersGained,subscribersLost,likes,comments,shares',
            filters=f'video=={video_id}',
            sort='day'
        ).execute()

        rows = response.get('rows', [])
        daily_data = []

        for row in rows:
            daily_data.append({
                'date': row[0],
                'views': int(row[1]),
                'watch_time_min': round(float(row[2]), 2),
                'avg_view_duration_sec': round(float(row[3]), 2),
                'avg_view_pct': round(float(row[4]), 2),
                'subs_gained': int(row[5]),
                'subs_lost': int(row[6]),
                'likes': int(row[7]),
                'comments': int(row[8]),
                'shares': int(row[9])
            })

        return daily_data
    except Exception as e:
        return []


def fetch_traffic_sources(video_id: str, start_date: str, end_date: str) -> list:
    """Fetch daily traffic source breakdown for a video."""
    analytics = get_analytics_service()
    if not analytics:
        return []

    try:
        response = analytics.reports().query(
            ids=f'channel=={YOUTUBE_CHANNEL_ID}',
            startDate=start_date,
            endDate=end_date,
            dimensions='day,insightTrafficSourceType',
            metrics='views',
            filters=f'video=={video_id}',
            sort='day,-views'
        ).execute()

        rows = response.get('rows', [])
        traffic_data = []

        for row in rows:
            views = int(row[2])
            if views > 0:
                traffic_data.append({
                    'date': row[0],
                    'source': row[1],
                    'views': views
                })

        return traffic_data
    except Exception:
        return []


def analyze_traffic_sources(traffic_data: list) -> dict:
    """Analyze traffic source patterns."""
    if not traffic_data:
        return {}

    # Group by source
    total_by_source = defaultdict(int)
    for d in traffic_data:
        total_by_source[d['source']] += d['views']

    total_views = sum(total_by_source.values())
    subscriber_views = total_by_source.get('SUBSCRIBER', 0)
    subscriber_pct = (subscriber_views / total_views * 100) if total_views > 0 else 0

    # Group by date for pattern analysis
    by_date = defaultdict(lambda: {'total': 0, 'subscriber': 0})
    for d in traffic_data:
        by_date[d['date']]['total'] += d['views']
        if d['source'] == 'SUBSCRIBER':
            by_date[d['date']]['subscriber'] += d['views']

    # Find peak subscriber day and algorithm boost
    peak_day = None
    peak_pct = 0
    algorithm_boost = False
    boost_days = []

    for date, data in sorted(by_date.items()):
        if data['total'] > 0:
            day_pct = data['subscriber'] / data['total'] * 100
            if day_pct > peak_pct:
                peak_pct = day_pct
                peak_day = date
            if day_pct > 80:
                algorithm_boost = True
                boost_days.append(date)

    return {
        'total_by_source': dict(total_by_source),
        'subscriber_pct': round(subscriber_pct, 1),
        'peak_subscriber_day': peak_day,
        'peak_subscriber_pct': round(peak_pct, 1),
        'algorithm_boost_detected': algorithm_boost,
        'boost_days': boost_days,
        'top_sources': sorted(total_by_source.items(), key=lambda x: x[1], reverse=True)[:5]
    }


# ============================================================================
# VIDEO PROCESSING (parallel-safe)
# ============================================================================

def process_single_video(video: dict, end_date: str) -> dict:
    """Fetch all analytics for a single video. Designed for parallel execution.
    The outer executor already parallelizes videos. Keep the three calls for each
    video sequential because googleapiclient service objects are not thread-safe.
    """
    video_id = video.get('id', '')
    snippet = video.get('snippet', {})
    stats = video.get('statistics', {})
    content = video.get('contentDetails', {})

    title = snippet.get('title', 'Untitled')
    published_at = snippet.get('publishedAt', '')

    try:
        pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
        start_date = pub_date.strftime('%Y-%m-%d')
        days_ago = (datetime.now() - pub_date.replace(tzinfo=None)).days
    except Exception:
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        days_ago = 365

    video_analytics = fetch_video_analytics(video_id, start_date, end_date)
    daily_data = fetch_daily_analytics(video_id, start_date, end_date)
    traffic_data = fetch_traffic_sources(video_id, start_date, end_date)

    video['analytics'] = video_analytics
    traffic_analysis = analyze_traffic_sources(traffic_data)

    total_views = sum(d['views'] for d in daily_data) if daily_data else int(stats.get('viewCount', 0))
    total_watch_time = sum(d['watch_time_min'] for d in daily_data) if daily_data else 0
    # The aggregate API value is view-weighted. Averaging daily percentages would
    # give a one-view day the same weight as a thousand-view day. Fall back to a
    # view-weighted daily value only when aggregate analytics are unavailable.
    if video_analytics.get('avg_view_percentage') is not None:
        avg_retention = float(video_analytics['avg_view_percentage'])
    elif daily_data and total_views > 0:
        avg_retention = sum(d['avg_view_pct'] * d['views'] for d in daily_data) / total_views
    else:
        avg_retention = 0
    def aggregate_or_daily(aggregate_key: str, daily_key: str) -> int:
        aggregate_value = video_analytics.get(aggregate_key)
        if aggregate_value is not None:
            return int(aggregate_value)
        return sum(int(d.get(daily_key, 0)) for d in daily_data)

    total_subs = aggregate_or_daily('subscribers_gained', 'subs_gained')
    total_subs_lost = aggregate_or_daily('subscribers_lost', 'subs_lost')
    total_likes = aggregate_or_daily('likes', 'likes')
    total_comments = aggregate_or_daily('comments', 'comments')
    total_shares = aggregate_or_daily('shares', 'shares')
    calendar_days = max(days_ago + 1, 1)
    views_per_day = total_views / calendar_days

    duration_min = parse_duration_minutes(content.get('duration', 'PT0S'))
    category = auto_categorize(title, snippet.get('description', ''))

    return {
        'video_id': video_id,
        'title': title,
        'publish_date': start_date,
        'days_tracked': calendar_days,
        'days_ago': days_ago,
        'total_views': total_views,
        'total_watch_time_min': round(total_watch_time, 1),
        'avg_retention_pct': round(avg_retention, 1),
        'total_subs_gained': total_subs,
        'total_subs_lost': total_subs_lost,
        'total_likes': total_likes,
        'total_comments': total_comments,
        'total_shares': total_shares,
        'views_per_day': round(views_per_day, 2),
        'duration_minutes': round(duration_min, 1),
        'category': category,
        'daily_data': daily_data,
        'traffic_data': traffic_data,
        'traffic_analysis': traffic_analysis,
        'algorithm_boost': traffic_analysis.get('algorithm_boost_detected', False)
    }


# ============================================================================
# PHASE 3: Pattern Analysis
# ============================================================================

def analyze_content_patterns(videos_data: list) -> dict:
    """Analyze patterns across all videos."""
    if not videos_data:
        return {}

    # Sort by different metrics
    by_views = sorted(videos_data, key=lambda x: x['total_views'], reverse=True)
    by_retention = sorted(videos_data, key=lambda x: x['avg_retention_pct'], reverse=True)
    by_subs = sorted(videos_data, key=lambda x: x['total_subs_gained'], reverse=True)
    by_velocity = sorted(videos_data, key=lambda x: x['views_per_day'], reverse=True)

    # Calculate averages
    avg_views = sum(v['total_views'] for v in videos_data) / len(videos_data)
    avg_retention = sum(v['avg_retention_pct'] for v in videos_data) / len(videos_data)
    avg_subs = sum(v['total_subs_gained'] for v in videos_data) / len(videos_data)

    # Identify top/bottom performers (quartiles)
    n = len(videos_data)
    top_quartile_idx = max(1, n // 4)
    bottom_quartile_idx = max(1, n // 4)

    top_performers = by_views[:top_quartile_idx]
    underperformers = by_views[-bottom_quartile_idx:]

    # Title pattern analysis
    title_patterns = analyze_title_patterns(videos_data)

    # Duration analysis
    duration_analysis = analyze_duration_patterns(videos_data)

    # Category analysis
    category_analysis = analyze_category_patterns(videos_data)

    return {
        'rankings': {
            'by_views': by_views,
            'by_retention': by_retention,
            'by_subs': by_subs,
            'by_velocity': by_velocity
        },
        'averages': {
            'views': round(avg_views, 1),
            'retention': round(avg_retention, 1),
            'subs': round(avg_subs, 1)
        },
        'top_performers': top_performers,
        'underperformers': underperformers,
        'title_patterns': title_patterns,
        'duration_analysis': duration_analysis,
        'category_analysis': category_analysis
    }


def analyze_title_patterns(videos_data: list) -> dict:
    """Analyze which title patterns correlate with success."""
    patterns = {
        'get_your_moneys_worth': {'regex': r"money'?s worth", 'videos': [], 'avg_views': 0},
        'guide': {'regex': r'\bguide\b', 'videos': [], 'avg_views': 0},
        'how_to': {'regex': r'\bhow to\b', 'videos': [], 'avg_views': 0},
        'year_tag': {'regex': r'\b202[4-9]\b', 'videos': [], 'avg_views': 0},
        'beginner': {'regex': r'\bbeginner\b', 'videos': [], 'avg_views': 0},
        'framework': {'regex': r'\bframework\b', 'videos': [], 'avg_views': 0},
        'stop_using': {'regex': r'\bstop using\b', 'videos': [], 'avg_views': 0},
    }

    import re
    for video in videos_data:
        title = video.get('title', '').lower()
        for pattern_name, pattern_data in patterns.items():
            if re.search(pattern_data['regex'], title, re.IGNORECASE):
                pattern_data['videos'].append(video)

    # Calculate averages for each pattern
    for pattern_name, pattern_data in patterns.items():
        if pattern_data['videos']:
            pattern_data['avg_views'] = sum(v['total_views'] for v in pattern_data['videos']) / len(pattern_data['videos'])
            pattern_data['count'] = len(pattern_data['videos'])

    # Sort by average views
    sorted_patterns = sorted(
        [(k, v) for k, v in patterns.items() if v['videos']],
        key=lambda x: x[1]['avg_views'],
        reverse=True
    )

    return {
        'patterns': patterns,
        'best_patterns': sorted_patterns[:3] if sorted_patterns else []
    }


def analyze_duration_patterns(videos_data: list) -> dict:
    """Analyze correlation between video duration and performance."""
    duration_buckets = {
        'short_0_10': {'min': 0, 'max': 10, 'videos': []},
        'medium_10_20': {'min': 10, 'max': 20, 'videos': []},
        'long_20_40': {'min': 20, 'max': 40, 'videos': []},
        'very_long_40+': {'min': 40, 'max': 999, 'videos': []},
    }

    for video in videos_data:
        duration_min = video.get('duration_minutes', 0)
        for bucket_name, bucket in duration_buckets.items():
            if bucket['min'] <= duration_min < bucket['max']:
                bucket['videos'].append(video)
                break

    # Calculate averages per bucket
    for bucket_name, bucket in duration_buckets.items():
        if bucket['videos']:
            bucket['avg_views'] = sum(v['total_views'] for v in bucket['videos']) / len(bucket['videos'])
            bucket['avg_retention'] = sum(v['avg_retention_pct'] for v in bucket['videos']) / len(bucket['videos'])
            bucket['count'] = len(bucket['videos'])

    # Find best bucket
    best_bucket = max(
        [(k, v) for k, v in duration_buckets.items() if v.get('count', 0) > 0],
        key=lambda x: x[1].get('avg_retention', 0),
        default=None
    )

    return {
        'buckets': duration_buckets,
        'best_bucket': best_bucket
    }


def analyze_category_patterns(videos_data: list) -> dict:
    """Analyze performance by video category."""
    categories = defaultdict(list)

    for video in videos_data:
        cat = video.get('category', 'Other')
        categories[cat].append(video)

    category_stats = {}
    for cat, videos in categories.items():
        if videos:
            category_stats[cat] = {
                'count': len(videos),
                'avg_views': sum(v['total_views'] for v in videos) / len(videos),
                'avg_retention': sum(v['avg_retention_pct'] for v in videos) / len(videos),
                'avg_subs': sum(v['total_subs_gained'] for v in videos) / len(videos),
                'total_subs': sum(v['total_subs_gained'] for v in videos)
            }

    # Sort by avg views
    sorted_cats = sorted(category_stats.items(), key=lambda x: x[1]['avg_views'], reverse=True)

    return {
        'stats': category_stats,
        'best_category': sorted_cats[0] if sorted_cats else None
    }


# ============================================================================
# PHASE 4: Generate Recommendations
# ============================================================================

def generate_recommendations(patterns: dict, traffic_analysis: dict, videos_data: list) -> list:
    """Generate actionable recommendations based on analysis."""
    recommendations = []

    # 1. Title pattern recommendations
    title_patterns = patterns.get('title_patterns', {}).get('best_patterns', [])
    if title_patterns:
        best_pattern = title_patterns[0]
        pattern_name = best_pattern[0].replace('_', ' ').title()
        avg_views = best_pattern[1].get('avg_views', 0)
        overall_avg = patterns.get('averages', {}).get('views', 1)
        multiplier = avg_views / overall_avg if overall_avg > 0 else 1

        if multiplier > 1.3:
            recommendations.append({
                'priority': 'high',
                'category': 'title',
                'recommendation': f"Use '{pattern_name}' title format - {multiplier:.1f}x higher views than average",
                'evidence': f"Videos with this pattern average {avg_views:.0f} views vs channel average of {overall_avg:.0f}"
            })

    # 2. Duration recommendations
    duration = patterns.get('duration_analysis', {})
    best_bucket = duration.get('best_bucket')
    if best_bucket:
        bucket_name = best_bucket[0]
        bucket_data = best_bucket[1]
        min_dur = bucket_data.get('min', 0)
        max_dur = bucket_data.get('max', 60)
        retention = bucket_data.get('avg_retention', 0)

        recommendations.append({
            'priority': 'medium',
            'category': 'duration',
            'recommendation': f"Target {min_dur}-{max_dur} minute videos - highest retention ({retention:.1f}%)",
            'evidence': f"{bucket_data.get('count', 0)} videos in this range with best engagement"
        })

    # 3. Category recommendations
    category = patterns.get('category_analysis', {})
    best_cat = category.get('best_category')
    if best_cat:
        cat_name = best_cat[0]
        cat_data = best_cat[1]
        if cat_data.get('total_subs', 0) > 0:
            recommendations.append({
                'priority': 'high',
                'category': 'content_type',
                'recommendation': f"Create more '{cat_name}' content - highest subscriber conversion",
                'evidence': f"{cat_data['total_subs']} total subs gained, {cat_data['avg_subs']:.1f} avg per video"
            })

    # 4. Traffic source recommendations
    boosted_videos = [v for v in videos_data if v.get('algorithm_boost')]
    if boosted_videos:
        recommendations.append({
            'priority': 'high',
            'category': 'algorithm',
            'recommendation': "Study algorithm-boosted videos for patterns to replicate",
            'evidence': f"{len(boosted_videos)} video(s) received algorithm boost (>80% SUBSCRIBER traffic)"
        })

    # 5. Underperformer recommendations
    underperformers = patterns.get('underperformers', [])
    if underperformers:
        recommendations.append({
            'priority': 'medium',
            'category': 'optimization',
            'recommendation': f"Optimize thumbnails/titles for {len(underperformers)} underperforming videos",
            'evidence': "These videos are below channel average - small improvements could yield significant gains"
        })

    # 6. Search optimization
    search_traffic = sum(
        v.get('traffic_analysis', {}).get('total_by_source', {}).get('YT_SEARCH', 0)
        for v in videos_data
    )
    total_traffic = sum(
        sum(v.get('traffic_analysis', {}).get('total_by_source', {}).values())
        for v in videos_data
    )
    search_pct = (search_traffic / total_traffic * 100) if total_traffic > 0 else 0

    if search_pct < 20:
        recommendations.append({
            'priority': 'medium',
            'category': 'seo',
            'recommendation': "Improve YouTube SEO - only {:.1f}% of views from search".format(search_pct),
            'evidence': "Optimizing titles and descriptions for search could unlock consistent organic traffic"
        })

    # Sort by priority
    priority_order = {'high': 0, 'medium': 1, 'low': 2}
    recommendations.sort(key=lambda x: priority_order.get(x['priority'], 3))

    return recommendations


# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_analysis_report(videos_data: list, patterns: dict, recommendations: list, output_folder: Path):
    """Generate comprehensive markdown analysis report."""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')

    # Build executive summary
    total_videos = len(videos_data)
    total_views = sum(v['total_views'] for v in videos_data)
    total_subs = sum(v['total_subs_gained'] for v in videos_data)
    boosted_count = len([v for v in videos_data if v.get('algorithm_boost')])

    rankings = patterns.get('rankings', {})
    top_by_views = rankings.get('by_views', [])[:1]
    top_by_retention = rankings.get('by_retention', [])[:1]

    report = f"""# YouTube Performance Analysis

**Generated**: {now}
**Videos Analyzed**: {total_videos}
**Total Views**: {total_views:,}
**Total Subscribers Gained**: {total_subs}

---

## Executive Summary

"""
    if top_by_views:
        v = top_by_views[0]
        report += f"- **Top Performer**: \"{v['title'][:50]}\" ({v['total_views']:,} views)\n"

    if top_by_retention:
        v = top_by_retention[0]
        report += f"- **Best Engagement**: \"{v['title'][:50]}\" ({v['avg_retention_pct']:.1f}% retention)\n"

    report += f"- **Algorithm Boosts**: {boosted_count} video(s) received significant algorithm push\n"
    report += f"- **Avg Views/Video**: {patterns.get('averages', {}).get('views', 0):.0f}\n"
    report += f"- **Avg Retention**: {patterns.get('averages', {}).get('retention', 0):.1f}%\n"

    # Performance rankings
    report += """
---

## Performance Rankings

### Top Performers (by Total Views)

| Rank | Title | Views | Retention | Subs |
|------|-------|-------|-----------|------|
"""
    for i, v in enumerate(rankings.get('by_views', [])[:5], 1):
        report += f"| {i} | {v['title'][:40]} | {v['total_views']:,} | {v['avg_retention_pct']:.1f}% | {v['total_subs_gained']} |\n"

    report += """
### Top Performers (by Retention)

| Rank | Title | Retention | Views | Subs |
|------|-------|-----------|-------|------|
"""
    for i, v in enumerate(rankings.get('by_retention', [])[:5], 1):
        report += f"| {i} | {v['title'][:40]} | {v['avg_retention_pct']:.1f}% | {v['total_views']:,} | {v['total_subs_gained']} |\n"

    report += """
### Best Subscriber Conversion

| Rank | Title | Subs Gained | Conversion Rate |
|------|-------|-------------|-----------------|
"""
    for i, v in enumerate(rankings.get('by_subs', [])[:5], 1):
        conv_rate = (v['total_subs_gained'] / v['total_views'] * 100) if v['total_views'] > 0 else 0
        report += f"| {i} | {v['title'][:40]} | {v['total_subs_gained']} | {conv_rate:.2f}% |\n"

    # Underperformers
    underperformers = patterns.get('underperformers', [])
    if underperformers:
        report += """
### Attention Needed (Underperformers)

| Title | Views | Retention | Potential Issue |
|-------|-------|-----------|-----------------|
"""
        avg_views = patterns.get('averages', {}).get('views', 0)
        avg_retention = patterns.get('averages', {}).get('retention', 0)

        for v in underperformers[:5]:
            issue = []
            if v['total_views'] < avg_views * 0.5:
                issue.append("Low views")
            if v['avg_retention_pct'] < avg_retention * 0.8:
                issue.append("Low retention")
            issue_str = ", ".join(issue) if issue else "Below average"
            report += f"| {v['title'][:40]} | {v['total_views']:,} | {v['avg_retention_pct']:.1f}% | {issue_str} |\n"

    # Traffic Source Analysis
    report += """
---

## Traffic Source Analysis

### Overall Traffic Mix

| Source | Description | Total Views |
|--------|-------------|-------------|
"""
    # Aggregate traffic sources
    total_by_source = defaultdict(int)
    for v in videos_data:
        ta = v.get('traffic_analysis', {}).get('total_by_source', {})
        for source, views in ta.items():
            total_by_source[source] += views

    source_descriptions = {
        'SUBSCRIBER': 'YouTube homepage/notifications',
        'YT_SEARCH': 'YouTube search results',
        'RELATED_VIDEO': 'Suggested videos sidebar',
        'EXT_URL': 'External websites/Google',
        'PLAYLIST': 'Playlist plays',
        'YT_CHANNEL': 'Your channel page',
        'NO_LINK_OTHER': 'Direct/mobile apps',
        'NOTIFICATION': 'Push notifications'
    }

    for source, views in sorted(total_by_source.items(), key=lambda x: x[1], reverse=True):
        desc = source_descriptions.get(source, source)
        report += f"| {source} | {desc} | {views:,} |\n"

    # Algorithm boost section
    boosted = [v for v in videos_data if v.get('algorithm_boost')]
    if boosted:
        report += f"""
### Algorithm Boost Detected

**{len(boosted)} video(s) received algorithm boost** (>80% SUBSCRIBER traffic on peak days)

| Video | Subscriber % | Peak Day |
|-------|--------------|----------|
"""
        for v in boosted:
            ta = v.get('traffic_analysis', {})
            report += f"| {v['title'][:40]} | {ta.get('subscriber_pct', 0):.1f}% | {ta.get('peak_subscriber_day', 'N/A')} |\n"

        report += """
**What This Means:**
- SUBSCRIBER traffic = YouTube pushing your video on homepages
- Algorithm typically tests for 48 hours, then boosts for ~7 days if metrics are good
- Early retention in first 48 hours triggers the cascade
"""

    # What's Working
    report += """
---

## What's Working

"""
    title_patterns = patterns.get('title_patterns', {}).get('best_patterns', [])
    if title_patterns:
        report += "### Title Patterns That Perform\n\n"
        for pattern_name, pattern_data in title_patterns:
            count = pattern_data.get('count', 0)
            avg = pattern_data.get('avg_views', 0)
            report += f"- **{pattern_name.replace('_', ' ').title()}**: {count} videos, {avg:.0f} avg views\n"
        report += "\n"

    category = patterns.get('category_analysis', {}).get('best_category')
    if category:
        cat_name, cat_data = category
        report += f"### Best Performing Category\n\n"
        report += f"**{cat_name}** - {cat_data['count']} videos\n"
        report += f"- Avg Views: {cat_data['avg_views']:.0f}\n"
        report += f"- Avg Retention: {cat_data['avg_retention']:.1f}%\n"
        report += f"- Total Subs: {cat_data['total_subs']}\n\n"

    duration = patterns.get('duration_analysis', {}).get('best_bucket')
    if duration:
        bucket_name, bucket_data = duration
        report += f"### Optimal Video Length\n\n"
        report += f"**{bucket_data['min']}-{bucket_data['max']} minutes** performs best\n"
        report += f"- {bucket_data.get('count', 0)} videos in this range\n"
        report += f"- Avg Retention: {bucket_data.get('avg_retention', 0):.1f}%\n\n"

    # What's NOT Working
    report += """---

## What's NOT Working

"""
    if underperformers:
        report += f"### {len(underperformers)} Underperforming Video(s)\n\n"
        report += "Videos below channel average that could benefit from optimization:\n\n"
        for v in underperformers[:3]:
            report += f"- \"{v['title'][:50]}\" - {v['total_views']} views, {v['avg_retention_pct']:.1f}% retention\n"
        report += "\n"

    # Recommendations
    report += """---

## Actionable Recommendations

"""
    high_priority = [r for r in recommendations if r['priority'] == 'high']
    medium_priority = [r for r in recommendations if r['priority'] == 'medium']

    if high_priority:
        report += "### High Priority\n\n"
        for i, r in enumerate(high_priority, 1):
            report += f"{i}. **{r['recommendation']}**\n"
            report += f"   - *Evidence*: {r['evidence']}\n\n"

    if medium_priority:
        report += "### Medium Priority\n\n"
        for i, r in enumerate(medium_priority, len(high_priority) + 1):
            report += f"{i}. **{r['recommendation']}**\n"
            report += f"   - *Evidence*: {r['evidence']}\n\n"

    # Save report
    filepath = output_folder / "analysis_report.md"
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report)

    return filepath


# ============================================================================
# NOTION SYNC
# ============================================================================

def sync_to_notion(videos: list) -> tuple:
    """Sync videos to Notion database. Returns (created, updated) counts."""
    if not YOUTUBE_NOTION_DB_ID:
        return 0, 0

    # Fetch existing Notion records
    existing = {}
    cursor = None

    while True:
        payload = {"page_size": 100}
        if cursor:
            payload["start_cursor"] = cursor

        response = requests.post(
            f"{NOTION_BASE_URL}/databases/{YOUTUBE_NOTION_DB_ID}/query",
            headers=NOTION_HEADERS,
            json=payload
        )
        data = response.json()

        for record in data.get("results", []):
            video_id_prop = record.get("properties", {}).get("Video ID", {}).get("rich_text", [])
            if video_id_prop:
                vid = video_id_prop[0].get("text", {}).get("content", "")
                if vid:
                    existing[vid] = record["id"]

        if not data.get("has_more"):
            break
        cursor = data.get("next_cursor")

    def sync_one(video):
        video_id = video.get('id', '')
        snippet = video.get('snippet', {})
        stats = video.get('statistics', {})

        properties = {
            "Video Title": {"title": [{"text": {"content": snippet.get('title', 'Untitled')}}]},
            "Video ID": {"rich_text": [{"text": {"content": video_id}}]},
            "Video URL": {"url": f"https://www.youtube.com/watch?v={video_id}"},
            "Views": {"number": int(stats.get('viewCount', 0))},
            "Likes": {"number": int(stats.get('likeCount', 0))},
            "Comments": {"number": int(stats.get('commentCount', 0))},
        }

        analytics = video.get('analytics', {})
        if analytics.get('watch_time_minutes'):
            properties["Watch Time (min)"] = {"number": analytics['watch_time_minutes']}
        if analytics.get('avg_view_percentage'):
            properties["Avg % Viewed"] = {"number": analytics['avg_view_percentage'] / 100}
        if analytics.get('subscribers_gained'):
            properties["Subs Gained"] = {"number": analytics['subscribers_gained']}

        if video_id in existing:
            requests.patch(
                f"{NOTION_BASE_URL}/pages/{existing[video_id]}",
                headers=NOTION_HEADERS,
                json={"properties": properties}
            )
            return 'updated'
        else:
            requests.post(
                f"{NOTION_BASE_URL}/pages",
                headers=NOTION_HEADERS,
                json={"parent": {"database_id": YOUTUBE_NOTION_DB_ID}, "icon": {"type": "emoji", "emoji": "📹"}, "properties": properties}
            )
            return 'created'

    # Notion rate limit is 3 req/sec — use 3 workers
    with ThreadPoolExecutor(max_workers=3) as executor:
        results = list(executor.map(sync_one, videos))

    created = results.count('created')
    updated = results.count('updated')
    return created, updated


# ============================================================================
# CSV EXPORTS
# ============================================================================

def export_csvs(videos_data: list, output_folder: Path):
    """Export all data to CSV files."""
    # Summary CSV
    summary_path = output_folder / "all_videos_summary.csv"
    with open(summary_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'video_id', 'title', 'publish_date', 'days_tracked',
            'total_views', 'total_watch_time_min', 'avg_retention_pct',
            'total_subs_gained', 'total_subs_lost', 'total_likes',
            'total_comments', 'total_shares', 'views_per_day',
            'subscriber_pct', 'algorithm_boost', 'category'
        ])
        writer.writeheader()
        for v in videos_data:
            writer.writerow({
                'video_id': v['video_id'],
                'title': v['title'],
                'publish_date': v['publish_date'],
                'days_tracked': v['days_tracked'],
                'total_views': v['total_views'],
                'total_watch_time_min': v['total_watch_time_min'],
                'avg_retention_pct': v['avg_retention_pct'],
                'total_subs_gained': v['total_subs_gained'],
                'total_subs_lost': v['total_subs_lost'],
                'total_likes': v['total_likes'],
                'total_comments': v['total_comments'],
                'total_shares': v['total_shares'],
                'views_per_day': v['views_per_day'],
                'subscriber_pct': v.get('traffic_analysis', {}).get('subscriber_pct', 0),
                'algorithm_boost': v.get('algorithm_boost', False),
                'category': v.get('category', 'Other')
            })

    # Per-video daily CSVs
    for v in videos_data:
        if v.get('daily_data'):
            daily_path = output_folder / f"{v['video_id']}_daily.csv"
            with open(daily_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=[
                    'date', 'views', 'watch_time_min', 'avg_view_duration_sec',
                    'avg_view_pct', 'subs_gained', 'subs_lost',
                    'likes', 'comments', 'shares'
                ])
                writer.writeheader()
                writer.writerows(v['daily_data'])

        if v.get('traffic_data'):
            traffic_path = output_folder / f"{v['video_id']}_traffic.csv"
            with open(traffic_path, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['date', 'source', 'views'])
                writer.writeheader()
                writer.writerows(v['traffic_data'])


# ============================================================================
# UTILITIES
# ============================================================================

def parse_duration_minutes(duration: str) -> float:
    """Convert ISO 8601 duration to minutes."""
    import re
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 60 + minutes + seconds / 60


def auto_categorize(title: str, description: str) -> str:
    """Auto-categorize video based on title/description."""
    text = f"{title} {description}".lower()

    if any(w in text for w in ["money's worth", 'guide to', 'how to use', 'getting started']):
        return "AI Tool Guide"
    if any(w in text for w in ['framework', 'strategy', 'like a beginner', 'mindset']):
        return "AI Framework"
    if any(w in text for w in ['review', 'changed everything', 'comparison', 'vs']):
        return "AI Tool Review"
    if any(w in text for w in ['step by step', 'tutorial', 'walkthrough']):
        return "Tutorial"
    return "Other"


# ============================================================================
# MAIN
# ============================================================================

def main():
    import time
    t_total = time.time()

    parser = argparse.ArgumentParser(description='Comprehensive YouTube Performance Analysis')
    parser.add_argument('--skip-notion', action='store_true', help='Skip Notion sync')
    parser.add_argument('--video-id', help='Analyze specific video only')
    args = parser.parse_args()

    print("\n" + "=" * 80)
    print("YOUTUBE PERFORMANCE ANALYSIS")
    print("=" * 80 + "\n")

    # Validate config
    if not YOUTUBE_API_KEY:
        print("❌ Missing YOUTUBE_API_KEY in .env")
        return

    # Check Analytics API
    analytics = get_analytics_service()
    if not analytics:
        print("\n⚠️  Running without Analytics API - limited analysis available\n")
    else:
        print("✓ Analytics API connected\n")

    # Create output folder
    today = datetime.now().strftime('%Y%m%d')
    output_folder = WORKSPACE / '.tmp' / f'youtube_analysis_{today}'
    output_folder.mkdir(parents=True, exist_ok=True)

    # ========================================================================
    # PHASE 1: Data Collection
    # ========================================================================
    t1 = time.time()
    print("[Phase 1] Fetching videos and current metrics...")

    videos = fetch_youtube_videos()
    if args.video_id:
        videos = [v for v in videos if v.get('id') == args.video_id]

    print(f"✓ Found {len(videos)} video(s)  [{time.time() - t1:.1f}s]")

    # ========================================================================
    # PHASE 2: Historical Analytics (parallel)
    # ========================================================================
    t2 = time.time()
    print("\n[Phase 2] Fetching historical analytics (parallel)...")

    # Validate credentials in the main thread. Each worker lazily creates its own
    # thread-local Analytics service; service objects must never cross threads.
    get_analytics_service()
    get_youtube_service()

    end_date = datetime.now().strftime('%Y-%m-%d')
    videos_data = []
    total_data_points = 0

    # Process videos in parallel. Each worker makes a video's three Analytics API
    # calls sequentially on that worker's thread-local service.
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_video = {
            executor.submit(process_single_video, video, end_date): video
            for video in videos
        }
        completed = 0
        for future in as_completed(future_to_video):
            completed += 1
            source_video = future_to_video[future]
            try:
                video_data = future.result()
            except Exception as exc:
                video_id = source_video.get('id', 'unknown')
                title = source_video.get('snippet', {}).get('title', video_id)
                print(f"   [{completed}/{len(videos)}] ⚠️  Skipped {title[:50]} ({video_id}): {exc}")
                continue
            videos_data.append(video_data)
            status = "🚀" if video_data.get('algorithm_boost') else "✓"
            days = video_data['days_tracked']
            print(f"   [{completed}/{len(videos)}] {video_data['title'][:50]} {status} ({days} days)")
            total_data_points += days

    # Restore original video order (parallel completion is non-deterministic)
    video_order = {v.get('id', ''): i for i, v in enumerate(videos)}
    videos_data.sort(key=lambda vd: video_order.get(vd['video_id'], 999))

    # Attach analytics back to original video objects for Notion sync
    analytics_by_id = {vd['video_id']: vd for vd in videos_data}
    for video in videos:
        vd = analytics_by_id.get(video.get('id', ''))
        if vd:
            video['analytics'] = {
                'watch_time_minutes': vd['total_watch_time_min'],
                'avg_view_percentage': vd['avg_retention_pct'],
                'subscribers_gained': vd['total_subs_gained'],
            }

    print(f"\n✓ Collected {total_data_points} days of data across {len(videos_data)} videos  [{time.time() - t2:.1f}s]")

    # Sync to Notion (after analytics collected so retention/watch time/subs are included)
    if not args.skip_notion and YOUTUBE_NOTION_DB_ID:
        t_notion = time.time()
        created, updated = sync_to_notion(videos)
        print(f"✓ Synced to Notion: {created} created, {updated} updated  [{time.time() - t_notion:.1f}s]")

    # ========================================================================
    # PHASE 3: Pattern Analysis
    # ========================================================================
    t3 = time.time()
    print("\n[Phase 3] Analyzing patterns...")

    patterns = analyze_content_patterns(videos_data)

    boosted = [v for v in videos_data if v.get('algorithm_boost')]
    print(f"✓ {len(boosted)} video(s) detected with algorithm boost")

    search_videos = [v for v in videos_data
                     if v.get('traffic_analysis', {}).get('total_by_source', {}).get('YT_SEARCH', 0) > 10]
    print(f"✓ {len(search_videos)} video(s) getting YouTube search traffic  [{time.time() - t3:.1f}s]")

    # ========================================================================
    # PHASE 4: Generate Recommendations
    # ========================================================================
    t4 = time.time()
    print("\n[Phase 4] Generating recommendations...")

    # Aggregate traffic for recommendations
    all_traffic = {}
    for v in videos_data:
        ta = v.get('traffic_analysis', {})
        all_traffic.update(ta)

    recommendations = generate_recommendations(patterns, all_traffic, videos_data)
    print(f"✓ Generated {len(recommendations)} actionable recommendations  [{time.time() - t4:.1f}s]")

    # ========================================================================
    # EXPORT RESULTS
    # ========================================================================
    t5 = time.time()
    print("\n[Phase 5] Exporting results...")

    export_csvs(videos_data, output_folder)
    report_path = generate_analysis_report(videos_data, patterns, recommendations, output_folder)

    print(f"✓ Report saved: {report_path.relative_to(WORKSPACE)}")

    # ========================================================================
    # SUMMARY
    # ========================================================================
    print("\n" + "=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)

    rankings = patterns.get('rankings', {})
    by_views = rankings.get('by_views', [])
    by_retention = rankings.get('by_retention', [])

    if by_views:
        v = by_views[0]
        print(f"📈 Best Performer: \"{v['title'][:40]}\" ({v['total_views']:,} views, {v['avg_retention_pct']:.1f}% retention)")

    if boosted:
        print(f"🚀 Algorithm Favorites: {len(boosted)} video(s) got >80% SUBSCRIBER traffic")

    if search_videos:
        print(f"🔍 Search Winners: {len(search_videos)} video(s) getting consistent YT_SEARCH traffic")

    underperformers = patterns.get('underperformers', [])
    if underperformers:
        print(f"⚠️  Attention Needed: {len(underperformers)} video(s) underperforming")

    print("\n" + "=" * 80)
    print("TOP RECOMMENDATIONS")
    print("=" * 80)

    for i, r in enumerate(recommendations[:5], 1):
        print(f"{i}. {r['recommendation']}")

    print(f"\n📊 Full report: {output_folder.relative_to(WORKSPACE)}/analysis_report.md")
    print(f"⏱  Total time: {time.time() - t_total:.1f}s")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
