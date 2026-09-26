# Shopify blogs and articles

Official docs index: https://docs.zernio.com/llms.txt

Zernio proxies blog CRUD to the connected platform and stores no recoverable copy. The current live docs support Shopify accounts (`platform: "shopify"`). Other platforms return `400` or `405`.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| GET / POST | `/v1/accounts/{accountId}/blogs` | list or create blogs |
| GET / PATCH / DELETE | `/v1/accounts/{accountId}/blogs/{blogId}` | read, update, or permanently delete a blog |
| GET / POST | `/v1/accounts/{accountId}/blogs/{blogId}/articles` | list or create articles |
| GET / PATCH / DELETE | `/v1/accounts/{accountId}/blogs/{blogId}/articles/{articleId}` | read, update, or permanently delete an article |

List endpoints use cursor pagination with `limit` 1-50 and `nextCursor`.

## Article behavior

- `isPublished: false` creates a draft.
- A future ISO 8601 `publishDate` schedules natively on Shopify; it does not use the Zernio post queue.
- `bodyHtml` is HTML content. `seo.title` and `seo.description` map to Shopify's global SEO metafields.
- Featured-image URLs must be publicly reachable by Shopify.

## Safety

Creating/updating/publishing an article changes the connected store and requires confirmation of the exact account/blog, title/handle, body, author, SEO, image, draft/publish state, and time. Deleting an article is permanent; deleting a blog permanently deletes every article in it. List every exact target and obtain destructive confirmation immediately before deletion.

