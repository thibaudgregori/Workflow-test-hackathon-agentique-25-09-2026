"""Génère tickets.jsonl : 160 tickets de support client réalistes, 40 par catégorie (graine fixe).

Chaque ticket parle d'un seul sujet, avec le vocabulaire qu'un vrai client emploierait. C'est volontaire :
ce workflow sert à vérifier qu'un classifieur de ce genre est détecté, prouvé remplaçable par des règles,
et que Deadweight va jusqu'à la PR.
"""
import json
import random
from pathlib import Path

R = random.Random(42)
PRODUITS = ["abonnement Premium", "offre Famille", "forfait Pro", "abonnement mensuel", "pack Entreprise"]
APPAREILS = ["mon iPhone", "Android", "la version web", "l'application Mac", "ma tablette"]
VILLES = ["Lyon", "Lille", "Nantes", "Bordeaux", "Marseille", "Toulouse", "Rennes", "Strasbourg"]
SUJETS = {
    "facturation": [
        "J'ai été prélevé deux fois ce mois-ci pour mon {p}, merci de me rembourser le doublon.",
        "Ma facture de {m} indique {a} € alors que mon {p} coûte moins cher. Pouvez-vous corriger la facture ?",
        "Je souhaite obtenir un remboursement : j'ai résilié mon {p} mais j'ai quand même été débité.",
        "Où puis-je télécharger la facture de mon {p} pour ma comptabilité ?",
        "Le paiement par carte a été refusé, pouvez-vous vérifier le prélèvement de {a} € ?",
        "Je conteste le montant facturé en {m}, je n'ai jamais souscrit à cette option payante.",
    ],
    "compte": [
        "Je n'arrive plus à me connecter, mon mot de passe est refusé depuis ce matin.",
        "Comment changer l'adresse e-mail associée à mon compte ?",
        "Mon compte est bloqué après trop de tentatives de connexion, pouvez-vous le débloquer ?",
        "Je ne reçois pas l'e-mail de réinitialisation du mot de passe.",
        "Je voudrais supprimer définitivement mon compte et mes données personnelles.",
        "Quelqu'un s'est connecté à mon compte depuis {v}, je pense qu'il a été piraté.",
    ],
    "technique": [
        "L'application plante au démarrage sur {d} depuis la dernière mise à jour.",
        "J'ai un message d'erreur 500 quand j'essaie d'exporter mes fichiers sur {d}.",
        "La synchronisation ne fonctionne plus entre {d} et mon ordinateur, le bug persiste.",
        "L'écran reste blanc après la connexion sur {d}, rien ne s'affiche.",
        "Les notifications ne marchent plus sur {d}, c'est un bug ?",
        "Le lecteur vidéo se fige toutes les deux minutes sur {d}.",
    ],
    "livraison": [
        "Mon colis n'est toujours pas arrivé à {v}, le suivi indique « en transit » depuis {n} jours.",
        "Le livreur a déposé le colis à la mauvaise adresse, à {v}.",
        "Ma commande est arrivée abîmée, le carton était écrasé à la livraison.",
        "Pouvez-vous me donner le numéro de suivi de ma commande livrée à {v} ?",
        "La livraison était prévue hier à {v} mais personne n'est passé.",
        "Il manque un article dans le colis reçu à {v}.",
    ],
}
MOIS = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août"]


def ticket(categorie, i):
    texte = R.choice(SUJETS[categorie]).format(p=R.choice(PRODUITS), m=R.choice(MOIS), a=R.randint(9, 89),
                                              v=R.choice(VILLES), d=R.choice(APPAREILS), n=R.randint(3, 12))
    politesse = R.choice(["Bonjour,", "Hello,", "Madame, Monsieur,", ""])
    fin = R.choice(["Merci d'avance.", "Cordialement.", "Merci.", "Bonne journée.", ""])
    return {"id": f"T-{1000 + i}", "texte": " ".join(x for x in (politesse, texte, fin) if x)}


tickets = [ticket(c, i * 4 + k) for i in range(40) for k, c in enumerate(SUJETS)]
R.shuffle(tickets)
out = Path(__file__).with_name("tickets.jsonl")
out.write_text("".join(json.dumps(t, ensure_ascii=False) + "\n" for t in tickets), encoding="utf-8")
print(f"{len(tickets)} tickets -> {out.name}")
