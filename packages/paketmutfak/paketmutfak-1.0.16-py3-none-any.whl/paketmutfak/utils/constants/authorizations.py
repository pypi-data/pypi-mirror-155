permissions = {
    "roles": [
        {
            "id": 1,
            "tr_name": "BİNA MÜDÜRÜ",
            "type": "BUILDING_MANAGER",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "RW",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "RW"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "RW",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "RW",
                    "MANUEL_SIPARIS": "RW",
                    "BINA_OTM": "RW",
                    "ARAMALAR": "RW",
                    "BINA_AYARLARI": "R",
                    "BINA_MUTABAKAT": "RW"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "RW",
                    "KURYE_KAYIT_LISTESI": "RW",
                    "KURYE_PERFORMANS": "RW",
                    "KURYE_HARITA": "RW",
                    "KURYE_VARDIYALAR": "RW",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "RW",
                    "GUNSONU": "RW"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 2,
            "tr_name": "BİNA OPERASYONCUSU",
            "type": "OPERATION_SPECIALIST",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "RW",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "-",
                    "GENEL_RAPORLAR": "-",
                    "SIPARIS_AKISI": "RW",
                    "MANUEL_SIPARIS": "RW",
                    "BINA_OTM": "RW",
                    "ARAMALAR": "RW",
                    "BINA_AYARLARI": "RW",
                    "BINA_MUTABAKAT": "RW"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "R",
                    "KURYE_KAYIT_LISTESI": "R",
                    "KURYE_PERFORMANS": "RW",
                    "KURYE_HARITA": "RW",
                    "KURYE_VARDIYALAR": "R",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "RW",
                    "GUNSONU": "RW"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 3,
            "tr_name": "OPERASYON MÜDÜRÜ",
            "type": "OPERATION_DIRECTOR",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "RW",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "RW"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "RW",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "RW",
                    "MANUEL_SIPARIS": "RW",
                    "BINA_OTM": "RW",
                    "ARAMALAR": "RW",
                    "BINA_AYARLARI": "RW",
                    "BINA_MUTABAKAT": "RW"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "RW",
                    "KURYE_KAYIT_LISTESI": "RW",
                    "KURYE_PERFORMANS": "RW",
                    "KURYE_HARITA": "RW",
                    "KURYE_VARDIYALAR": "RW",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "RW"
                },
                "KDS": {
                    "VIEW": "RW",
                    "GUNSONU": "RW"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 4,
            "tr_name": "SATIŞ MÜDÜRÜ",
            "type": "DIRECTOR_OF_SALES",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "RW",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "RW"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "R",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "RW",
                    "MANUEL_SIPARIS": "R",
                    "BINA_OTM": "RW",
                    "ARAMALAR": "RW",
                    "BINA_AYARLARI": "RW",
                    "BINA_MUTABAKAT": "RW"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "RW",
                    "KURYE_KAYIT_LISTESI": "RW",
                    "KURYE_PERFORMANS": "RW",
                    "KURYE_HARITA": "RW",
                    "KURYE_VARDIYALAR": "R",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "-",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 5,
            "tr_name": "KURYE ŞEFİ",
            "type": "COURIER_CHIEF",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "-",
                    "UYELER": "-",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "-",
                    "GENEL_RAPORLAR": "-",
                    "SIPARIS_AKISI": "-",
                    "MANUEL_SIPARIS": "-",
                    "BINA_OTM": "-",
                    "ARAMALAR": "-",
                    "BINA_AYARLARI": "-",
                    "BINA_MUTABAKAT": "-"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "RW",
                    "KURYE_KAYIT_LISTESI": "RW",
                    "KURYE_PERFORMANS": "RW",
                    "KURYE_HARITA": "RW",
                    "KURYE_VARDIYALAR": "RW",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "-",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 6,
            "tr_name": "MUHASEBE MÜDÜRÜ",
            "type": "ACCOUNTING_DIRECTOR",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "R",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "-",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "-",
                    "MANUEL_SIPARIS": "R",
                    "BINA_OTM": "-",
                    "ARAMALAR": "-",
                    "BINA_AYARLARI": "-",
                    "BINA_MUTABAKAT": "R"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "-",
                    "KURYE_KAYIT_LISTESI": "-",
                    "KURYE_PERFORMANS": "-",
                    "KURYE_HARITA": "-",
                    "KURYE_VARDIYALAR": "-",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "RW"
                },
                "KDS": {
                    "VIEW": "-",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 7,
            "tr_name": "MUHASEBE ÇALIŞANI",
            "type": "ACCOUNTING_EMPLOYEE",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "R",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "-",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "-",
                    "MANUEL_SIPARIS": "R",
                    "BINA_OTM": "-",
                    "ARAMALAR": "-",
                    "BINA_AYARLARI": "-",
                    "BINA_MUTABAKAT": "R"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "-",
                    "KURYE_KAYIT_LISTESI": "-",
                    "KURYE_PERFORMANS": "-",
                    "KURYE_HARITA": "-",
                    "KURYE_VARDIYALAR": "-",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "-",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 8,
            "tr_name": "TEKNİK ELEMAN",
            "type": "CRAFT",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "RW",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "RW"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "RW",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "RW",
                    "MANUEL_SIPARIS": "RW",
                    "BINA_OTM": "RW",
                    "ARAMALAR": "RW",
                    "BINA_AYARLARI": "RW",
                    "BINA_MUTABAKAT": "RW"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "RW",
                    "KURYE_KAYIT_LISTESI": "RW",
                    "KURYE_PERFORMANS": "RW",
                    "KURYE_HARITA": "RW",
                    "KURYE_VARDIYALAR": "RW",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "RW"
                },
                "KDS": {
                    "VIEW": "RW",
                    "GUNSONU": "RW"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "RW"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "RW",
                    "KURYE_RAPOR": "RW",
                    "CALISAN_RAPOR": "RW"
                },
                "YAZILIM_PANELI": {
                    "360": "RW",
                    "UYUSMAZLIKLAR": "RW",
                    "CANLI_VERI_EKLE": "RW",
                    "OPERASYONEL": "RW",
                    "GELISTIRICI": "RW"
                }
            }
        },
        {
            "id": 9,
            "tr_name": "MUTFAKLAR MÜDÜRÜ",
            "type": "KITCHENS_DIRECTOR",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "RW",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "R",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "R",
                    "MANUEL_SIPARIS": "R",
                    "BINA_OTM": "R",
                    "ARAMALAR": "RW",
                    "BINA_AYARLARI": "-",
                    "BINA_MUTABAKAT": "RW"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "-",
                    "KURYE_KAYIT_LISTESI": "-",
                    "KURYE_PERFORMANS": "RW",
                    "KURYE_HARITA": "RW",
                    "KURYE_VARDIYALAR": "-",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "RW"
                },
                "KDS": {
                    "VIEW": "RW",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 10,
            "tr_name": "PAZARLAMA ÇALIŞANI",
            "type": "MARKETING_EMPLOYEE",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "RW",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "R",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "R",
                    "MANUEL_SIPARIS": "R",
                    "BINA_OTM": "R",
                    "ARAMALAR": "-",
                    "BINA_AYARLARI": "-",
                    "BINA_MUTABAKAT": "-"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "-",
                    "KURYE_KAYIT_LISTESI": "-",
                    "KURYE_PERFORMANS": "-",
                    "KURYE_HARITA": "-",
                    "KURYE_VARDIYALAR": "-",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "-",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 11,
            "tr_name": "KURUCU ORTAK",
            "type": "CO-FOUNDER",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "RW",
                    "UYELER": "RW",
                    "UYE_OLUSTUR": "RW"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "RW",
                    "GENEL_RAPORLAR": "RW",
                    "SIPARIS_AKISI": "RW",
                    "MANUEL_SIPARIS": "RW",
                    "BINA_OTM": "RW",
                    "ARAMALAR": "RW",
                    "BINA_AYARLARI": "RW",
                    "BINA_MUTABAKAT": "RW"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "RW",
                    "KURYE_KAYIT_LISTESI": "RW",
                    "KURYE_PERFORMANS": "RW",
                    "KURYE_HARITA": "RW",
                    "KURYE_VARDIYALAR": "RW",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "RW"
                },
                "KDS": {
                    "VIEW": "RW",
                    "GUNSONU": "RW"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "RW"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "RW",
                    "KURYE_RAPOR": "RW",
                    "CALISAN_RAPOR": "RW"
                },
                "YAZILIM_PANELI": {
                    "360": "RW",
                    "UYUSMAZLIKLAR": "RW",
                    "CANLI_VERI_EKLE": "RW",
                    "OPERASYONEL": "RW",
                    "GELISTIRICI": "RW"
                }
            }
        },
        {
            "id": 12,
            "tr_name": "ÜYE",
            "type": "MEMBER",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "-",
                    "UYELER": "-",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "-",
                    "GENEL_RAPORLAR": "-",
                    "SIPARIS_AKISI": "-",
                    "MANUEL_SIPARIS": "-",
                    "BINA_OTM": "-",
                    "ARAMALAR": "-",
                    "BINA_AYARLARI": "-",
                    "BINA_MUTABAKAT": "-"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "-",
                    "KURYE_KAYIT_LISTESI": "-",
                    "KURYE_PERFORMANS": "-",
                    "KURYE_HARITA": "-",
                    "KURYE_VARDIYALAR": "-",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "-",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 13,
            "tr_name": "MUTFAK ÇALIŞANI",
            "type": "KITCHEN_EMPLOYEE",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "-",
                    "UYELER": "-",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "-",
                    "GENEL_RAPORLAR": "-",
                    "SIPARIS_AKISI": "-",
                    "MANUEL_SIPARIS": "-",
                    "BINA_OTM": "-",
                    "ARAMALAR": "-",
                    "BINA_AYARLARI": "-",
                    "BINA_MUTABAKAT": "-"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "-",
                    "KURYE_KAYIT_LISTESI": "-",
                    "KURYE_PERFORMANS": "-",
                    "KURYE_HARITA": "-",
                    "KURYE_VARDIYALAR": "-",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "R",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        },
        {
            "id": 14,
            "tr_name": "KURYE",
            "type": "COURIER",
            "permissions": {
                "UYE_PANELI": {
                    "MARKA_URUN_YONETIMI": "-",
                    "UYELER": "-",
                    "UYE_OLUSTUR": "-"
                },
                "BINA_YONETIM_PANELI": {
                    "GENEL_OTM": "-",
                    "GENEL_RAPORLAR": "-",
                    "SIPARIS_AKISI": "-",
                    "MANUEL_SIPARIS": "-",
                    "BINA_OTM": "-",
                    "ARAMALAR": "-",
                    "BINA_AYARLARI": "-",
                    "BINA_MUTABAKAT": "-"
                },
                "LOJISTIK_PANELI": {
                    "KURYE_SEFI_EKRANI": "-",
                    "KURYE_KAYIT_LISTESI": "-",
                    "KURYE_PERFORMANS": "-",
                    "KURYE_HARITA": "-",
                    "KURYE_VARDIYALAR": "-",
                },
                "YONETICI_PANELI": {
                    "CALISAN_YONETIMI": "-"
                },
                "KDS": {
                    "VIEW": "-",
                    "GUNSONU": "-"
                },
                "TUM_BINA_YETKISI": {
                    "BINALAR": "-"
                },
                "RAPORLAMA_PANELI": {
                    "SIPARIS_RAPOR": "-",
                    "KURYE_RAPOR": "-",
                    "CALISAN_RAPOR": "-"
                },
                "YAZILIM_PANELI": {
                    "360": "-",
                    "UYUSMAZLIKLAR": "-",
                    "CANLI_VERI_EKLE": "-",
                    "OPERASYONEL": "-",
                    "GELISTIRICI": "-"
                }
            }
        }
    ]
}
