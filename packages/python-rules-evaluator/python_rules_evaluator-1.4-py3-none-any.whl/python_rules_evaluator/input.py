DOC = {
    "_id": "P02908-1_12_121786614_T_C",
    "_cls": "BaseVariant.SnvVariant",
    "analysed": True,
    "causative": False,
    "change": {
        "ref": {
            "base": "T",
            "allelic_depth": None
        },
        "alt": {
            "base": "C",
            "allelic_depth": None
        }
    },
    "check_de_novo": False,
    "chromosome": "12",
    "comment": "#ROW: 5010\n\nRELEVANCIA DE LA VARIANTE PARA EL PROBANDO\nVariante en un gen consistentemente asociado a fenotipos audiológicos dominantes. Analizar mediante ACMG.\n\nINTERPRETACIÓN CLÍNICA DE LA VARIANTE\nVariante no sinónima en heterozigosis que afecta a un residuo conservado.\nDG score 0,48. 0,000399 (1000 Genomes). REVEL score 0,126.\nVariante en el dominio Smac_DIABLO (10-239 aa), con ésta como única variante benigna en el dominio según ClinVar.\n\nAusente en HGMD.\nEn ClinVar como PB por 1 submitter.\nAusente en Google Scholar.\n\nCriterios ACMG\nPatogenicidad:\nPVS1: No lo cumple.\nPS1: No lo cumple.\nPS2: No lo cumple.\nPS3: No lo cumple.\nPS4: No lo cumple.\nPM1: No lo cumple.\nPM2: No lo cumple.\nPM3: No lo cumple.\nPM4: No aplica.\nPM5: No lo cumple.\nPM6: No lo cumple.\nPP1: No lo cumple.\nPP2: -\nPP3: No lo cumple.\nPP4: No lo cumple.\nPP5: -\n\nBenignidad:\nBS1: Lo cumple.\n0,0004 > 0,0002 (AD)\nBS2: No lo cumple.\nBS3: No lo cumple.\nBS4: No lo cumple.\nBP1: -\nBP2: No lo cumple.\nBP3: No aplica.\nBP4: Lo cumple.\nBP5: Lo cumple. (presente en este caso, IM19-0385, resuelto por la variante COCH c.263G>C p.Gly88Ala)\nBP6: -\nBP7: No aplica.\n\nEn base a los criterios ACMG (BS1, BP4, BP5) la variante es PROBABLEMENTE BENIGNA.\nRevisada 08/01/2020",
    "created_ts": "2021-09-01T09:04:29.222Z",
    "custom_report_table": "AUTO",
    "de_novo": None,
    "de_novo_information": {
        "mother": {
            "checked": False,
            "parenthood_confirmed": False,
            "variant_absent": False
        },
        "father": {
            "checked": False,
            "parenthood_confirmed": False,
            "variant_absent": False
        }
    },
    "frequency": 0.48014440433212996,
    "genes": [
        {
            "gene": "DIABLO",
            "strand": ".",
            "pathways": [
                "."
            ],
            "hsir": False,
            "tier": 1,
            "phenotypes": {
                "custom": [
                    {
                        "phenotype": "Hipoacusia no sindrómica/DFNA64",
                        "reference": ".",
                        "inheritance_mode": "AD",
                        "disease": ".",
                        "candidate": False,
                        "notes": "",
                        "acmg": {
                            "PVS1": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 4,
                                "calculated_strength": 4,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_very_strong": "None (autopvs1_strength) == 'VeryStrong'",
                                    "cond_strong": "None (autopvs1_strength) == 'Strong'",
                                    "cond_moderate": "None (autopvs1_strength) == 'Moderate'",
                                    "cond_supporting": "None (autopvs1_strength) == 'Supporting'",
                                    "cond_match": [
                                        {
                                            "or": [
                                                "False (PVS1.very_strong)",
                                                "False (PVS1.strong)",
                                                "False (PVS1.moderate)",
                                                "False (PVS1.supporting)"
                                            ]
                                        }
                                    ]
                                },
                                "description": "Variante inactivadora en un gen en el cual la perdida de función es un mecanismo conocido de enfermedad."
                            },
                            "PS1": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 3,
                                "calculated_strength": 3,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True,
                                    "cond_strong": [
                                        {
                                            "or": [
                                                "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', chromosome='12 (chromosome)', position=121786614 (position), alt='C (alt)', ref='T (ref)', protein_change='p.Ile59Val (protein_change)', acmg_classification=['LP', 'P'] ) > 0",
                                              {
                                                  "and": [
                                                      "False (splicing_impact)",
                                                      "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', chromosome='12 (chromosome)', position=121786614 (position), alt='C (alt)', ref='T (ref)', splicing_type__contains=['splicing', 'canonical'], mes_diff__lte=None (max_ent_scan_diff), acmg_classification=['LP', 'P'] ) > 0"
                                                  ]
                                              }
                                            ]
                                        }
                                    ],
                                    "cond_match": [
                                        {
                                            "or": [
                                                "False (PS1.strong)"
                                            ]
                                        }
                                    ]
                                },
                                "description": None
                            },
                            "PS2": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 3,
                                "calculated_strength": 3,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True,
                                    "cond_very_strong": "0 (PC_points) >= 4",
                                    "cond_strong": "0 (PC_points) >= 2 and 0 (PC_points) < 4",
                                    "cond_moderate": "0 (PC_points) >= 1 and 0 (PC_points) < 2",
                                    "cond_supporting": "0 (PC_points) >= 0.5 and 0 (PC_points) < 1",
                                    "cond_match": [
                                        {
                                            "and": [
                                              {
                                                  "or": [
                                                      "False (PS2.very_strong)",
                                                      "False (PS2.strong)",
                                                      "False (PS2.moderate)",
                                                      "False (PS2.supporting)"
                                                  ]
                                              }
                                            ]
                                        }
                                    ]
                                },
                                "description": "Se trata de una variante de novo en un paciente sin historia familiar de la enfermedad."
                            },
                            "PS3": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 3,
                                "calculated_strength": 3,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True,
                                    "cond_strong": "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', chromosome='12 (chromosome)', position=121786614 (position), alt='C (alt)', ref='T (ref)', PS3_state=1, PS3_strength=3 ) > 0",
                                    "cond_moderate": "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', chromosome='12 (chromosome)', position=121786614 (position), alt='C (alt)', ref='T (ref)', PS3_state=1, PS3_strength=2 ) > 0",
                                    "cond_supporting": "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', chromosome='12 (chromosome)', position=121786614 (position), alt='C (alt)', ref='T (ref)', PS3_state=1, PS3_strength=1 ) > 0",
                                    "cond_match": [
                                        {
                                            "or": [
                                                "False (PS3.strong)",
                                                "False (PS3.moderate)",
                                                "False (PS3.supporting)"
                                            ]
                                        }
                                    ]
                                },
                                "description": "Estudios funcionales in vitro o in vivo sólidamente establecidos apoyan un efecto deletéreo de la variante en el gen o el producto del gen"
                            },
                            "PS4": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 3,
                                "calculated_strength": 3,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_not_applicable": [
                                        {
                                            "or": [
                                                "False (mitochondrial)"
                                            ]
                                        }
                                    ],
                                    "cond_needs_manual_input": True,
                                    "cond_strong": [
                                        {
                                            "and": [
                                                "False (PM2.match)",
                                                "True (dominant)",
                                                "0 (count_same_gene_and_dna_change) >= 15"
                                            ]
                                        }
                                    ],
                                    "cond_moderate": [
                                        {
                                            "and": [
                                                "False (PM2.match)",
                                                "True (dominant)",
                                                "0 (count_same_gene_and_dna_change) >= 6"
                                            ]
                                        }
                                    ],
                                    "cond_supporting": [
                                        {
                                            "and": [
                                                "False (PM2.match)",
                                                "True (dominant)",
                                                "0 (count_same_gene_and_dna_change) >= 2"
                                            ]
                                        }
                                    ],
                                    "cond_match": [
                                        {
                                            "or": [
                                                "False (PS4.strong)",
                                                "False (PS4.moderate)",
                                                "False (PS4.supporting)"
                                            ]
                                        }
                                    ]
                                },
                                "description": "La prevalencia de la variante en individuos afectos es significativamente mayor que la prevalencia en controles."
                            },
                            "PM1": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 2,
                                "calculated_strength": 2,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True,
                                    "cond_moderate": "('None (hotspot_region)' == 'hotspot_region')",
                                    "cond_match": "False (PM1.moderate)"
                                },
                                "description": "La variante está localizada en un hot-spot mutacional y/o un dominio funcional sólidamente establecido sin variación benigna."
                            },
                            "PM2": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_supporting": [
                                        {
                                            "or": [
                                              {
                                                  "and": [
                                                      "True (dominant)",
                                                      "0.000399361 (maf) <= 2e-05 (pm2_supporting_maf_limit_dominant)"
                                                  ]
                                              },
                                                {
                                                  "and": [
                                                      "False (recessive)",
                                                      "0.000399361 (maf) < 0.0007 (pm2_supporting_maf_limit_recessive)"
                                                  ]
                                              }
                                            ]
                                        }
                                    ],
                                    "cond_match": [
                                        {
                                            "or": [
                                                "False (PM2.supporting)"
                                            ]
                                        }
                                    ]
                                },
                                "description": "Se trata de una variante ausente en individuos control."
                            },
                            "PM3": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 2,
                                "calculated_strength": 2,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_not_applicable": "False (mitochondrial)",
                                    "cond_needs_manual_input": True,
                                    "cond_very_strong": [
                                        {
                                            "and": [
                                                "False (recessive)",
                                                "0 (PM3_points) >= 4"
                                            ]
                                        }
                                    ],
                                    "cond_strong": [
                                        {
                                            "and": [
                                                "False (recessive)",
                                                "0 (PM3_points) >= 2 and 0 (PM3_points) < 4"
                                            ]
                                        }
                                    ],
                                    "cond_moderate": [
                                        {
                                            "and": [
                                                "False (recessive)",
                                                "0 (PM3_points) >= 1 and 0 (PM3_points) < 2"
                                            ]
                                        }
                                    ],
                                    "cond_supporting": [
                                        {
                                            "and": [
                                                "False (recessive)",
                                                "0 (PM3_points) >= 0.5 and 0 (PM3_points) < 1"
                                            ]
                                        }
                                    ],
                                    "cond_match": [
                                        {
                                            "or": [
                                                "False (PM3.very_strong)",
                                                "False (PM3.strong)",
                                                "False (PM3.moderate)",
                                                "False (PM3.supporting)"
                                            ]
                                        }
                                    ]
                                },
                                "description": "Para enfermedades recesivas, la variante ha sido descrita en heterozigosis, heterozigosis compuesta y/u homocigosis en, al menos, otro paciente."
                            },
                            "PM4": {
                                "calculated_state": 0,
                                "state": -2,
                                "strength": 2,
                                "calculated_strength": 2,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_moderate": [
                                        {
                                            "and": [
                                                "(not False (PVS1.match))",
                                                "('None (repetitive_region)' != 'repetitive_region')",
                                              {
                                                  "or": [
                                                      "('inframe' in . (impact))",
                                                      "('stop_lost' in . (impact))"
                                                  ]
                                              }
                                            ]
                                        }
                                    ],
                                    "cond_match": "False (PM4.moderate)"
                                },
                                "description": None
                            },
                            "PM5": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 2,
                                "calculated_strength": 2,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True,
                                    "cond_moderate": [
                                        {
                                            "or": [
                                              {
                                                  "and": [
                                                      "('missense' in . (impact))",
                                                      "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', codon=None (codon), impact__contains=['missense'], acmg_classification=['LP', 'P'], protein_change__ne='p.Ile59Val (protein_change)', __distinct=['protein_change'] ) == 1"
                                                  ]
                                              },
                                                {
                                                  "and": [
                                                      "('. (impact)' in ['splice_region_variant','splice_acceptor_variant','splice_donor_variant','splice_branch_variant'])",
                                                      "('canonical' not in '. (splicing_type)')",
                                                      "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', splicing_type__contains=['splicing', 'canonical'], dna_change__ne='c.175A>G (dna_change)', acmg_classification=['LP', 'P'] ) == 1"
                                                  ]
                                              }
                                            ]
                                        }
                                    ],
                                    "cond_strong": [
                                        {
                                            "or": [
                                                {
                                                    "and": [
                                                        "('missense' in . (impact))",
                                                        "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', codon=None (codon), impact__contains=['missense'], acmg_classification=['LP', 'P'], protein_change__ne='p.Ile59Val (protein_change)', __distinct=['protein_change'] ) >= 2"
                                                    ]
                                                },
                                                {
                                                    "and": [
                                                        "('. (splicing_type)' in ['splicing', 'splicing_syn', 'splicing_nonsyn'])",
                                                        "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', splicing_type__contains=['splicing'], dna_change__ne='c.175A>G (dna_change)', acmg_classification=['LP', 'P'], ) >= 2"
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "cond_match": [
                                        {
                                            "or": [
                                                "False (PM5.moderate)",
                                                "False (PM5.strong)"
                                            ]
                                        }
                                    ]
                                },
                                "description": "Se ha descrito al menos otra variante no sinónima que afecta al mismo aminoácido y que ha sido considerada como patogénica."
                            },
                            "PM6": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 2,
                                "calculated_strength": 2,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True,
                                    "cond_very_strong": "0 (PC_points) >= 4",
                                    "cond_strong": "0 (PC_points) >= 2 and 0 (PC_points) < 4",
                                    "cond_moderate": "0 (PC_points) >= 1 and 0 (PC_points) < 2",
                                    "cond_supporting": "0 (PC_points) >= 0.5 and 0 (PC_points) < 1",
                                    "cond_match": [
                                        {
                                            "and": [
                                              {
                                                  "or": [
                                                      "False (PM6.very_strong)",
                                                      "False (PM6.strong)",
                                                      "False (PM6.moderate)",
                                                      "False (PM6.supporting)"
                                                  ]
                                              }
                                            ]
                                        }
                                    ]
                                },
                                "description": "Variante asumida de novo en un paciente sin historia familiar de la enfermedad."
                            },
                            "PP1": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True,
                                    "cond_supporting": [
                                        {
                                            "or": [
                                              {
                                                  "and": [
                                                      "True (dominant)",
                                                      "None (segregation) == 2 (pp1_supporting_dominant_segregation_limit)"
                                                  ]
                                              },
                                                {
                                                  "and": [
                                                      "False (recessive)",
                                                      "None (segregation) == 1 (pp1_supporting_recessive_segregation_limit)"
                                                  ]
                                              }
                                            ]
                                        }
                                    ],
                                    "cond_moderate": [
                                        {
                                            "or": [
                                                {
                                                    "and": [
                                                        "True (dominant)",
                                                        "None (segregation) == 4 (pp1_moderate_dominant_segregation_limit)"
                                                    ]
                                                },
                                                {
                                                    "and": [
                                                        "False (recessive)",
                                                        "None (segregation) == 2 (pp1_moderate_recessive_segregation_limit)"
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "cond_strong": [
                                        {
                                            "or": [
                                                {
                                                    "and": [
                                                        "True (dominant)",
                                                        "None (segregation) == 5 (pp1_strong_dominant_segregation_limit)"
                                                    ]
                                                },
                                                {
                                                    "and": [
                                                        "False (recessive)",
                                                        "None (segregation) == 3 (pp1_strong_recessive_segregation_limit)"
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "cond_match": [
                                        {
                                            "or": [
                                                "False (PP1.strong)",
                                                "False (PP1.moderate)",
                                                "False (PP1.supporting)"
                                            ]
                                        }
                                    ]
                                },
                                "description": "Cosegregación de la variante con la enfermedad en múltiples miembros afectos de una familia/varias familias en un gen claramente causante de la enfermedad."
                            },
                            "PP2": {
                                "calculated_state": -1,
                                "state": -1,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {},
                                "description": "Variante no sinónima en un gen con baja tasa de variación no sinónima benigna y en el cual las variantes no sinónimas son un mecanismo común de la enfermedad."
                            },
                            "PP3": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_supporting": [
                                        {
                                            "or": [
                                                "None (revel_score) >= 0.7 (pp3_revel_score_limit)",
                                                "False (splicing_impact)"
                                            ]
                                        }
                                    ],
                                    "cond_match": "False (PP3.supporting)"
                                },
                                "description": "La evaluación bioinformática de la variante predice un efecto funcional deletéreo."
                            },
                            "PP4": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True
                                },
                                "description": "El fenotipo del paciente se asocia de manera altamente específica con el gen."
                            },
                            "PPC": {
                                "calculated_state": -1,
                                "state": -1,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {},
                                "description": None
                            },
                            "BA1": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 0,
                                "calculated_strength": 0,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_standalone": [
                                        {
                                            "or": [
                                              {
                                                  "and": [
                                                      "True (dominant)",
                                                      "0.000399361 (maf) >= 0.001 (ba1_maf_limit_dominant)"
                                                  ]
                                              },
                                                {
                                                  "and": [
                                                      "False (recessive)",
                                                      "0.000399361 (maf) >= 0.005 (ba1_maf_limit_recessive)"
                                                  ]
                                              }
                                            ]
                                        }
                                    ],
                                    "cond_match": "False (BA1.standalone)"
                                },
                                "description": "Variante que puede ser considerada benigna por su alta frecuencia alélica."
                            },
                            "BS1": {
                                "calculated_state": 1,
                                "state": 1,
                                "strength": 3,
                                "calculated_strength": 3,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_strong": [
                                        {
                                            "or": [
                                              {
                                                  "and": [
                                                      "True (dominant)",
                                                      "0.000399361 (maf) >= 0.0002 (bs1_strong_maf_limit_dominant)"
                                                  ]
                                              },
                                                {
                                                  "and": [
                                                      "False (recessive)",
                                                      "0.000399361 (maf) >= 0.003 (bs1_strong_maf_limit_recessive)"
                                                  ]
                                              }
                                            ]
                                        }
                                    ],
                                    "cond_supporting": [
                                        {
                                            "and": [
                                                "False (recessive)",
                                                "0.000399361 (maf) >= 0.0007 (bs1_supporting_maf_limit_recessive)"
                                            ]
                                        }
                                    ],
                                    "cond_match": [
                                        {
                                            "or": [
                                                "True (BS1.strong)",
                                                "False (BS1.supporting)"
                                            ]
                                        }
                                    ]
                                },
                                "description": "La frecuencia alélica de la variante es superior a la esperada para la enfermedad."
                            },
                            "BS2": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 3,
                                "calculated_strength": 3,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True
                                },
                                "description": "Observada en un individuo adulto sano para una enfermedad dominante (heterozigoto) con penetrancia completa esperada a temprana edad."
                            },
                            "BS3": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 3,
                                "calculated_strength": 3,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True
                                },
                                "description": "Estudios funcionales in vitro o in vivo sólidamente establecidos muestran un efecto no patogénico de la variante en la función de la proteína o en el splicing."
                            },
                            "BS4": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 3,
                                "calculated_strength": 3,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True
                                },
                                "description": "Ausencia de cosegregación en miembros afectos de la familia."
                            },
                            "BP1": {
                                "calculated_state": 0,
                                "state": -1,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True
                                },
                                "description": "Variante no sinónima en un gen para el cual las variantes causantes de enfermedad conocidas son principalmente variantes truncantes."
                            },
                            "BP2": {
                                "calculated_state": 0,
                                "state": 0,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_needs_manual_input": True,
                                    "cond_not_applicable": [
                                        {
                                            "or": "('DIABLO (gene)' == '')"
                                        }
                                    ],
                                    "cond_supporting": [
                                        {
                                            "or": [
                                                "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', chromosome='12 (chromosome)', position=121786614 (position), alt='C (alt)', ref='T (ref)', __in_cis_variant_same_gene_classification=['LP', 'P'] ) > 0",
                                                {
                                                    "and": [
                                                        "True (dominant)",
                                                        "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', chromosome='12 (chromosome)', position=121786614 (position), alt='C (alt)', ref='T (ref)', __in_trans_variant_same_gene_classification=['LP', 'P'] ) > 0"
                                                    ]
                                                }
                                            ]
                                        }
                                    ],
                                    "cond_match": "False (BP2.supporting)"
                                },
                                "description": "Observada en trans con una variante patogénica en un gen/enfermedad con penetrancia completa u observada en cis con una variante patogénica para cualquier modo de herencia."
                            },
                            "BP3": {
                                "calculated_state": 0,
                                "state": -2,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_supporting": [
                                        {
                                            "and": [
                                                "None (repetitive_region) == \"repetitive_region\"",
                                                "SNV (variant_sub_type) == \"InDel\"",
                                                "len(None (protein_domain)) == 0",
                                                "('inframe' in . (impact))"
                                            ]
                                        }
                                    ],
                                    "cond_match": "False (BP3.supporting)"
                                },
                                "description": "Inserción/deleción en pauta en una región repetitiva sin función conocida."
                            },
                            "BP4": {
                                "calculated_state": 0,
                                "state": 1,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_supporting": [
                                        {
                                            "or": [
                                                "None (revel_score) <= 0.15 (bp4_revel_score_limit)",
                                                "False (splicing_impact) == False"
                                            ]
                                        }
                                    ],
                                    "cond_match": "False (BP4.supporting)"
                                },
                                "description": "La evaluación bioinformática de la variante no predice un efecto funcional deletéreo."
                            },
                            "BP5": {
                                "calculated_state": 0,
                                "state": 1,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_supporting": [
                                        {
                                            "or": [
                                              {
                                                  "and": [
                                                      "('None (zygosity)' == 'HOMOZYGOUS')",
                                                      "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', acmg_classification=['LP', 'P'], phenotype='Hipoacusia no sindrómica/DFNA64 (phenotype)', __is_dominant=True ) > 0"
                                                  ]
                                              },
                                                {
                                                  "and": [
                                                      "('None (zygosity)' == 'HETEROZYGOUS')",
                                                      "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', acmg_classification=['LP', 'P'], phenotype='Hipoacusia no sindrómica/DFNA64 (phenotype)', __is_dominant=True ) > 0",
                                                      {
                                                          "or": [
                                                              "True (dominant)",
                                                              "\\@history_count( variant_id='P02908-1_12_121786614_T_C (variant_id)', gene='DIABLO (gene)', zygosity='HETEROZYGOUS', phenotype='Hipoacusia no sindrómica/DFNA64 (phenotype)', in_trans_variants='P02908-1_12_121786614_T_C (variant_id)' ) > 0"
                                                          ]
                                                      }
                                                  ]
                                              }
                                            ]
                                        }
                                    ],
                                    "cond_match": "False (BP5.supporting)"
                                },
                                "description": "Variante identificada en un caso con una causa alternativa de enfermedad."
                            },
                            "BP7": {
                                "calculated_state": 0,
                                "state": -2,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {
                                    "cond_supporting": [
                                        {
                                            "and": [
                                                "('synonymous_variant' in . (impact))",
                                                "False (splicing_impact) == False"
                                            ]
                                        }
                                    ],
                                    "cond_match": "False (BP7.supporting)"
                                },
                                "description": "Variante sinónima para la que los algoritmos predictores de efecto en el splicing consideran que la variante no tiene efecto en el splicing."
                            },
                            "BPC": {
                                "calculated_state": -1,
                                "state": -1,
                                "strength": 1,
                                "calculated_strength": 1,
                                "comment": "",
                                "reviser_comment": "",
                                "info": {},
                                "evaluation": {},
                                "description": None
                            },
                            "calculated_classification": "US",
                            "classification": "LB"
                        },
                        "separated_analysis": False,
                        "phenotypic_consistency": "NOT_CONSISTENT",
                        "override_to_vus": False,
                        "analyse": True,
                        "calculated_analyse": False
                    }
                ],
                "omim": [
                    {
                        "phenotype": "Deafness, autosomal dominant 64",
                        "reference": ".",
                        "inheritance_mode": "AD",
                        "disease": ".",
                        "candidate": False,
                        "notes": "",
                        "separated_analysis": False,
                        "phenotypic_consistency": "NOT_EVALUATED",
                        "override_to_vus": False,
                        "analyse": False,
                        "calculated_analyse": False
                    }
                ],
                "orpha": []
            },
            "annotations":
                {
                    "_cls": "SnvAnnotation",
                    "id": "b41b1748272bb147754a70b97e14a01b",
                    "rank": 1,
                    "num_P": None,
                    "num_LP": None,
                    "impact": ".",
                    "variant_sub_type": "SNV",
                    "selected": True,
                    "ensembl_id": ".",
                    "ref_seq_id": "NM_019887",
                    "dna_change": "c.175A>G",
                    "protein_change": "p.Ile59Val",
                    "codon": 59,
                    "revel_score": None,
                    "rf_score": None,
                    "ada_score": None,
                    "affected_exon": ".",
                    "max_ent_scan": {
                        "ref_score": None,
                        "alt_score": None,
                        "diff_score": None
                    },
                    "protein_domains": [],
                    "protein_predictions": [
                        "Smac_DIABLO"
                    ],
                    "clinical_significances": [
                        "LIKELY_BENIGN"
                    ],
                    "variant_ids": [
                        "rs574777883"
                    ],
                    "maf": {
                        "values": [],
                        "max": 0.000399361,
                        "max_subpop": None
                    },
                    "splicing_type": ".",
                    "autopvs1_strength": None
            },
            "mitochondrial": False
        }
    ],
    "genotype": ".",
    "hgmd": {
        "variant_class": "Absent",
        "phenotype": "",
        "date": "2020-01-20T00:00:00.000Z"
    },
    "last_modify_user": "history_importer",
    "patient_info": {
        "patient_id": "IMXX-4993",
        "gender": "M"
    },
    "position": 121786614,
    "read_depth": 554,
    "report_table": "ACMG",
    "sealed": True,
    "test_id": "P02908-1",
    "validation_required": False,
    "variant_type": "SNV",
    "zygosity": "HETEROZYGOUS"
}
