DEVICE_ID = 5

REGIONS = {
    'single': {
        'name':    (1336, 99, 1613, 144),
        'pokemon': [
            (1375, 158, 1616, 266),
            (1375, 284, 1616, 392),
            (1375, 410, 1616, 518),
            (1375, 536, 1616, 644),
            (1375, 662, 1616, 770),
            (1375, 788, 1616, 896),
        ],
    },
    'double': {
        'name':    (1563, 95, 1845, 141),
        'pokemon': [
            (1603, 156, 1844, 264),
            (1603, 282, 1844, 390),
            (1603, 408, 1844, 516),
            (1603, 534, 1844, 642),
            (1603, 660, 1844, 768),
            (1603, 786, 1844, 894),
        ],
    },
}

# 出力ファイルパス
OUTPUT_POKEMON = "output_pokemon.png"

# OBSソース名
OBS_NAME_SOURCE    = "pokecham_auto-name"  # テキスト (GDI+) ソース
OBS_POKEMON_SOURCE = "pokecham_auto-poke"  # 画像ソース

# OCR言語設定 ('ja', 'en', 'ch_tra', 'ch_sim', 'ko' から選択)
OCR_LANGUAGES = ['ja', 'en']

# ホットキー設定
HOTKEY_CAPTURE = "F9"
HOTKEY_CLEAR   = "F10"
HOTKEY_SWITCH  = "F8"
