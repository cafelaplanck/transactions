#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 17:39:21 2022

@author: emilejetzer
"""

import sys

from datetime import datetime

import pandas as pd

if len(sys.argv) > 1:
    nom_csv = sys.argv[1]
else:
    print('Donner le nom d\'un fichier de transactions Desjardins en format CSV.')

nom_xlsx = datetime.now().isoformat().replace(':', '_') + '.xlsx'

# Ouvrir le fichier
relevé = pd.read_csv(nom_csv,
                     sep=',',
                     skiprows=2,
                     encoding='latin-1',
                     usecols=(3, 5, 7, 8, 13),
                     names=('date', 'description', 'retrait', 'depot', 'solde'))

# Simplifier les colonnes de transaction
relevé.loc[:, ['depot', 'retrait']] = relevé.loc[:, ['depot', 'retrait']]\
    .fillna(0)
relevé.loc[:, 'montant'] = relevé.depot - relevé.retrait

# Ajouter les colonnes du cahier des gérants
colonnes = ('facture', 'destinataire', 'catégorie', 'type', 'sous_total', 'tps',
            'tvq', 'total', 'variation_actif', 'actif_bancaire', 'variation_passif', 'passif', 'valeur')
relevé.loc[:, colonnes] = None

# Valeurs spécifiques
relevé.variation_actif = relevé.montant
relevé.actif_bancaire = relevé.solde
relevé.total = relevé.depot + relevé.retrait
relevé.sous_total = relevé.total / (1 + 0.05 + 0.09975)
relevé.tps = relevé.sous_total * 0.05
relevé.tvq = relevé.sous_total * 0.09975
relevé.loc[:, 'variation_passif'] = 0
relevé.loc[:, 'passif'] = 0
relevé.valeur = relevé.actif_bancaire - relevé.passif

# Déterminer le type, la catégorie et le destinataire, possiblement la facture


# Ajouter les colonnes pour le cahier des commandes
# colonnes = ('commande', 'envoi', 'fournisseur', 'montant_commandé',
#            'montant_facturé', 'réception', 'péremption')
#relevé.loc[:, colonnes] = None

# Remplir les valeurs pour le cahier des gérants


# Exporter la sortie
#relevé = relevé.loc[:, ['date', 'description', 'montant', 'solde']]
relevé.to_excel(nom_xlsx, index=False, encoding='utf-8')
