# Simple utility functions - no external dependencies

translations = {
    "en": {
        "app_title": "DGP Finance Pro",
        "app_subtitle": "Professional Financial Statement Generator",
        "settings": "Settings",
        "language": "Language",
        "org_type": "Organization Type"
    },
    "ar": {
        "app_title": "التمويل دي جي بي برو",
        "app_subtitle": "مولد البيانات المالية المهنية",
        "settings": "الإعدادات",
        "language": "اللغة",
        "org_type": "نوع المنظمة"
    },
    "zh": {
        "app_title": "DGP 财务专业版",
        "app_subtitle": "专业财务报表生成器",
        "settings": "设置",
        "language": "语言",
        "org_type": "组织类型"
    }
}

def get_translation(key, lang):
    if lang in translations and key in translations[lang]:
        return translations[lang][key]
    return translations.get("en", {}).get(key, key)

def set_language(lang):
    pass  # Handled via session state

def load_glossary():
    return {
        "assets": {"en": "Resources owned by the business.", "ar": "الموارد المملوكة للشركة."},
        "liabilities": {"en": "Obligations the business owes.", "ar": "الالتزامات المستحقة على الشركة."}
    }