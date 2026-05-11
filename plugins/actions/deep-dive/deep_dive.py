"""
title: Deep Dive
author: Fu-Jie
author_url: https://github.com/Fu-Jie/openwebui-extensions
funding_url: https://github.com/open-webui
version: 1.0.1
icon_url: data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9ImN1cnJlbnRDb2xvciIgc3Ryb2tlLXdpZHRoPSIyIiBzdHJva2UtbGluZWNhcD0icm91bmQiIHN0cm9rZS1saW5lam9pbj0icm91bmQiPjxwYXRoIGQ9Ik0xMiA3djE0Ii8+PHBhdGggZD0iTTMgMThhMSAxIDAgMCAxLTEtMVY0YTEgMSAwIDAgMSAxLTFoNWE0IDQgMCAwIDEgNCA0IDQgNCAwIDAgMSA0LTRoNWExIDEgMCAwIDEgMSAxdjEzYTEgMSAwIDAgMS0xIDFoLTZhMyAzIDAgMCAwLTMgMyAzIDMgMCAwIDAtMy0zeiIvPjxwYXRoIGQ9Ik02IDEyaDIiLz48cGF0aCBkPSJNMTYgMTJoMiIvPjwvc3ZnPg==
requirements: markdown
description: A comprehensive thinking lens that dives deep into any content - from context to logic, insights, and action paths.
"""

# Standard library imports
import asyncio
import re
import logging
from typing import Optional, Dict, Any, Callable, Awaitable
from datetime import datetime

# Third-party imports
from pydantic import BaseModel, Field
from fastapi import Request
import markdown

# OpenWebUI imports
from open_webui.utils.chat import generate_chat_completion
from open_webui.models.users import Users

# Logging setup
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# ── OpenWebUI version detection for async DB compatibility ──────────
try:
    from open_webui.env import VERSION as _owui_version
except ImportError:
    _owui_version = "0.0.0"


def _owui_version_ge(threshold: str) -> bool:
    try:
        v = [int(x) for x in _owui_version.split(".")[:3]]
        t = [int(x) for x in threshold.split(".")[:3]]
        return v >= t
    except (ValueError, TypeError):
        return False


async def _call_db(method, *args, **kwargs):
    if _owui_version_ge("0.9.0"):
        return await method(*args, **kwargs)
    else:
        return method(*args, **kwargs)

# =================================================================
# HTML Template - Process-Oriented Design with Theme Support
# =================================================================
HTML_WRAPPER_TEMPLATE = """
<!-- OPENWEBUI_PLUGIN_OUTPUT -->
<!DOCTYPE html>
<html lang="{user_language}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        :root {
            --dd-bg-primary: #ffffff;
            --dd-bg-secondary: #f8fafc;
            --dd-bg-tertiary: #f1f5f9;
            --dd-text-primary: #0f172a;
            --dd-text-secondary: #334155;
            --dd-text-dim: #64748b;
            --dd-border: #e2e8f0;
            --dd-accent: #3b82f6;
            --dd-accent-soft: #eff6ff;
            --dd-header-gradient: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            --dd-shadow: 0 10px 40px rgba(0,0,0,0.06);
            --dd-code-bg: #f1f5f9;
        }
        .theme-dark {
            --dd-bg-primary: #1e293b;
            --dd-bg-secondary: #0f172a;
            --dd-bg-tertiary: #334155;
            --dd-text-primary: #f1f5f9;
            --dd-text-secondary: #e2e8f0;
            --dd-text-dim: #94a3b8;
            --dd-border: #475569;
            --dd-accent: #60a5fa;
            --dd-accent-soft: rgba(59, 130, 246, 0.15);
            --dd-header-gradient: linear-gradient(135deg, #0f172a 0%, #1e1e2e 100%);
            --dd-shadow: 0 10px 40px rgba(0,0,0,0.3);
            --dd-code-bg: #334155;
        }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
            margin: 0; 
            padding: 10px; 
            background-color: transparent; 
        }
        #main-container { 
            display: flex; 
            flex-direction: column;
            gap: 24px; 
            width: 100%;
            max-width: 900px;
            margin: 0 auto;
        }
        .plugin-item { 
            background: var(--dd-bg-primary); 
            border-radius: 24px; 
            box-shadow: var(--dd-shadow); 
            overflow: hidden; 
            border: 1px solid var(--dd-border); 
        }
        /* STYLES_INSERTION_POINT */
    </style>
</head>
<body>
    <div id="main-container">
        <!-- CONTENT_INSERTION_POINT -->
    </div>
    <!-- SCRIPTS_INSERTION_POINT -->
    <script>
    (function() {
        const parseColorLuma = (colorStr) => {
            if (!colorStr) return null;
            let m = colorStr.match(/^#?([0-9a-f]{6})$/i);
            if (m) {
                const hex = m[1];
                const r = parseInt(hex.slice(0, 2), 16);
                const g = parseInt(hex.slice(2, 4), 16);
                const b = parseInt(hex.slice(4, 6), 16);
                return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
            }
            m = colorStr.match(/rgba?\\s*\\(\\s*(\\d+)\\s*,\\s*(\\d+)\\s*,\\s*(\\d+)/i);
            if (m) {
                const r = parseInt(m[1], 10);
                const g = parseInt(m[2], 10);
                const b = parseInt(m[3], 10);
                return (0.2126 * r + 0.7152 * g + 0.0722 * b) / 255;
            }
            return null;
        };
        const getThemeFromMeta = (doc) => {
            const metas = Array.from((doc || document).querySelectorAll('meta[name="theme-color"]'));
            if (!metas.length) return null;
            const color = metas[metas.length - 1].content.trim();
            const luma = parseColorLuma(color);
            if (luma === null) return null;
            return luma < 0.5 ? 'dark' : 'light';
        };
        const getParentDocumentSafe = () => {
            try {
                if (!window.parent || window.parent === window) return null;
                const pDoc = window.parent.document;
                void pDoc.title;
                return pDoc;
            } catch (err) { return null; }
        };
        const getThemeFromParentClass = () => {
            try {
                if (!window.parent || window.parent === window) return null;
                const pDoc = window.parent.document;
                const html = pDoc.documentElement;
                const body = pDoc.body;
                const htmlClass = html ? html.className : '';
                const bodyClass = body ? body.className : '';
                const htmlDataTheme = html ? html.getAttribute('data-theme') : '';
                if (htmlDataTheme === 'dark' || bodyClass.includes('dark') || htmlClass.includes('dark')) return 'dark';
                if (htmlDataTheme === 'light' || bodyClass.includes('light') || htmlClass.includes('light')) return 'light';
                return null;
            } catch (err) { return null; }
        };
        const setTheme = () => {
            const parentDoc = getParentDocumentSafe();
            const metaTheme = parentDoc ? getThemeFromMeta(parentDoc) : null;
            const parentClassTheme = getThemeFromParentClass();
            const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
            const chosen = metaTheme || parentClassTheme || (prefersDark ? 'dark' : 'light');
            document.documentElement.classList.toggle('theme-dark', chosen === 'dark');
        };
        setTheme();
        if (window.matchMedia) {
            window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', setTheme);
        }
    })();
    </script>
</body>
</html>
"""

# =================================================================
# i18n - Multi-language Support
# =================================================================

TRANSLATIONS = {
    "en-US": {
        "title": "Deep Dive Analysis",
        "badge": "Thinking Process",
        "phase_01": "Phase 01",
        "phase_02": "Phase 02",
        "phase_03": "Phase 03",
        "phase_04": "Phase 04",
        "context_label": "The Context",
        "logic_label": "The Logic",
        "insight_label": "The Insight",
        "path_label": "The Path",
        "word_count_label": "words",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "AI-Powered",
        "status_analyzing": "🌊 Deep Dive: Analyzing Context & Logic...",
        "status_complete": "🌊 Deep Dive complete!",
        "notification_initiating": "🌊 Initiating Deep Dive thinking process...",
        "notification_complete": "🌊 Deep Dive complete, {user_name}! Thinking chain generated.",
        "error_brief": "Content too brief ({length} chars). Deep Dive requires at least {min_length} chars for meaningful analysis.",
        "no_context": "No context extracted.",
        "no_logic": "No logic deconstructed.",
        "no_insight": "No insights found.",
        "no_path": "No path defined.",
        "no_items": "No items found.",
    },
    "zh-CN": {
        "title": "精读分析报告",
        "badge": "思维过程",
        "phase_01": "第一阶段",
        "phase_02": "第二阶段",
        "phase_03": "第三阶段",
        "phase_04": "第四阶段",
        "context_label": "全景 (The Context)",
        "logic_label": "脉络 (The Logic)",
        "insight_label": "洞察 (The Insight)",
        "path_label": "路径 (The Path)",
        "word_count_label": "字",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "AI 驱动分析",
        "status_analyzing": "🌊 深度下潜：正在分析背景与逻辑...",
        "status_complete": "🌊 深度下潜完成！",
        "notification_initiating": "🌊 正在启动深度下潜思维链...",
        "notification_complete": "🌊 深度下潜完成，{user_name}！思维链已生成。",
        "error_brief": "内容太短（{length} 字符）。深度下潜需要至少 {min_length} 字符才能进行有意义的分析。",
        "no_context": "未能提取全景信息。",
        "no_logic": "未能解构脉络。",
        "no_insight": "未能发现洞察。",
        "no_path": "未能定义路径。",
        "no_items": "未找到条目。",
    },
    "zh-HK": {
        "title": "精讀分析報告",
        "badge": "思維過程",
        "phase_01": "第一階段",
        "phase_02": "第二階段",
        "phase_03": "第三階段",
        "phase_04": "第四階段",
        "context_label": "全景 (The Context)",
        "logic_label": "脈絡 (The Logic)",
        "insight_label": "洞察 (The Insight)",
        "path_label": "路徑 (The Path)",
        "word_count_label": "字",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "AI 驅動分析",
        "status_analyzing": "🌊 深度下潛：正在分析背景與邏輯...",
        "status_complete": "🌊 深度下潛完成！",
        "notification_initiating": "🌊 正在啟動深度下潛思維鏈...",
        "notification_complete": "🌊 深度下潛完成，{user_name}！思維鏈已生成。",
        "error_brief": "內容太短（{length} 字符）。深度下潛需要至少 {min_length} 字符才能進行有意義的分析。",
        "no_context": "未能提取全景資訊。",
        "no_logic": "未能解構脈絡。",
        "no_insight": "未能發現洞察。",
        "no_path": "未能定義路徑。",
        "no_items": "未找到條目。",
    },
    "zh-TW": {
        "title": "精讀分析報告",
        "badge": "思維過程",
        "phase_01": "第一階段",
        "phase_02": "第二階段",
        "phase_03": "第三階段",
        "phase_04": "第四階段",
        "context_label": "全景 (The Context)",
        "logic_label": "脈絡 (The Logic)",
        "insight_label": "洞察 (The Insight)",
        "path_label": "路徑 (The Path)",
        "word_count_label": "字",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "AI 驅動分析",
        "status_analyzing": "🌊 深度下潛：正在分析背景與邏輯...",
        "status_complete": "🌊 深度下潛完成！",
        "notification_initiating": "🌊 正在啟動深度下潛思維鏈...",
        "notification_complete": "🌊 深度下潛完成，{user_name}！思維鏈已生成。",
        "error_brief": "內容太短（{length} 字符）。深度下潛需要至少 {min_length} 字符才能進行有意義的分析。",
        "no_context": "未能提取全景資訊。",
        "no_logic": "未能解構脈絡。",
        "no_insight": "未能發現洞察。",
        "no_path": "未能定義路徑。",
        "no_items": "未找到條目。",
    },
    "ja-JP": {
        "title": "ディープダイブ分析レポート",
        "badge": "思考プロセス",
        "phase_01": "フェーズ 01",
        "phase_02": "フェーズ 02",
        "phase_03": "フェーズ 03",
        "phase_04": "フェーズ 04",
        "context_label": "コンテキスト (The Context)",
        "logic_label": "ロジック (The Logic)",
        "insight_label": "インサイト (The Insight)",
        "path_label": "パス (The Path)",
        "word_count_label": "文字",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "AI駆動分析",
        "status_analyzing": "🌊 ディープダイブ：コンテキストとロジックを分析中...",
        "status_complete": "🌊 ディープダイブ完了！",
        "notification_initiating": "🌊 ディープダイブ思考プロセスを開始しています...",
        "notification_complete": "🌊 ディープダイブ完了、{user_name}さん！思考チェーンが生成されました。",
        "error_brief": "内容が短すぎます（{length}文字）。ディープダイブには最低{min_length}文字が必要です。",
        "no_context": "コンテキストが抽出されませんでした。",
        "no_logic": "ロジックが分解されませんでした。",
        "no_insight": "インサイトが見つかりませんでした。",
        "no_path": "パスが定義されませんでした。",
        "no_items": "項目が見つかりませんでした。",
    },
    "ko-KR": {
        "title": "심층 분석 보고서",
        "badge": "사고 과정",
        "phase_01": "단계 01",
        "phase_02": "단계 02",
        "phase_03": "단계 03",
        "phase_04": "단계 04",
        "context_label": "컨텍스트 (The Context)",
        "logic_label": "로직 (The Logic)",
        "insight_label": "통찰 (The Insight)",
        "path_label": "경로 (The Path)",
        "word_count_label": "단어",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "AI 기반 분석",
        "status_analyzing": "🌊 심층 분석: 컨텍스트 및 로직 분석 중...",
        "status_complete": "🌊 심층 분석 완료!",
        "notification_initiating": "🌊 심층 분석 사고 과정을 시작합니다...",
        "notification_complete": "🌊 심층 분석 완료, {user_name}님! 사고 체인이 생성되었습니다.",
        "error_brief": "내용이 너무 짧습니다 ({length}자). 심층 분석을 위해서는 최소 {min_length}자가 필요합니다.",
        "no_context": "컨텍스트가 추출되지 않았습니다.",
        "no_logic": "로직이 분석되지 않았습니다.",
        "no_insight": "통찰을 찾을 수 없습니다.",
        "no_path": "경로가 정의되지 않았습니다.",
        "no_items": "항목을 찾을 수 없습니다.",
    },
    "fr-FR": {
        "title": "Rapport d'Analyse Approfondie",
        "badge": "Processus de Réflexion",
        "phase_01": "Phase 01",
        "phase_02": "Phase 02",
        "phase_03": "Phase 03",
        "phase_04": "Phase 04",
        "context_label": "Le Contexte",
        "logic_label": "La Logique",
        "insight_label": "L'Aperçu",
        "path_label": "Le Chemin",
        "word_count_label": "mots",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "Propulsé par l'IA",
        "status_analyzing": "🌊 Deep Dive : Analyse du contexte et de la logique...",
        "status_complete": "🌊 Deep Dive terminé !",
        "notification_initiating": "🌊 Initialisation du processus de réflexion Deep Dive...",
        "notification_complete": "🌊 Deep Dive terminé, {user_name} ! Chaîne de réflexion générée.",
        "error_brief": "Contenu trop court ({length} caractères). Deep Dive nécessite au moins {min_length} caractères.",
        "no_context": "Aucun contexte extrait.",
        "no_logic": "Aucune logique déconstruite.",
        "no_insight": "Aucun aperçu trouvé.",
        "no_path": "Aucun chemin défini.",
        "no_items": "Aucun élément trouvé.",
    },
    "de-DE": {
        "title": "Tiefenanalyse-Bericht",
        "badge": "Denkprozess",
        "phase_01": "Phase 01",
        "phase_02": "Phase 02",
        "phase_03": "Phase 03",
        "phase_04": "Phase 04",
        "context_label": "Der Kontext",
        "logic_label": "Die Logik",
        "insight_label": "Die Erkenntnis",
        "path_label": "Der Pfad",
        "word_count_label": "Wörter",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "KI-gestützt",
        "status_analyzing": "🌊 Deep Dive: Kontext und Logik werden analysiert...",
        "status_complete": "🌊 Deep Dive abgeschlossen!",
        "notification_initiating": "🌊 Deep Dive Denkprozess wird eingeleitet...",
        "notification_complete": "🌊 Deep Dive abgeschlossen, {user_name}! Denkprozess wurde generiert.",
        "error_brief": "Inhalt zu kurz ({length} Zeichen). Deep Dive erfordert mindestens {min_length} Zeichen.",
        "no_context": "Kein Kontext extrahiert.",
        "no_logic": "Keine Logik dekonstruiert.",
        "no_insight": "Keine Erkenntnisse gefunden.",
        "no_path": "Kein Pfad definiert.",
        "no_items": "Keine Elemente gefunden.",
    },
    "es-ES": {
        "title": "Informe de Análisis Profundo",
        "badge": "Proceso de Pensamiento",
        "phase_01": "Fase 01",
        "phase_02": "Fase 02",
        "phase_03": "Fase 03",
        "phase_04": "Fase 04",
        "context_label": "El Contexto",
        "logic_label": "La Lógica",
        "insight_label": "La Perspicacia",
        "path_label": "El Camino",
        "word_count_label": "palabras",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "Potenciado por IA",
        "status_analyzing": "🌊 Deep Dive: Analizando contexto y lógica...",
        "status_complete": "🌊 Deep Dive completado!",
        "notification_initiating": "🌊 Iniciando el proceso de pensamiento Deep Dive...",
        "notification_complete": "🌊 Deep Dive completado, {user_name}! Cadena de pensamiento generada.",
        "error_brief": "Contenido demasiado breve ({length} caracteres). Deep Dive requiere al menos {min_length} caracteres.",
        "no_context": "No se extrajo contexto.",
        "no_logic": "No se deconstruyó la lógica.",
        "no_insight": "No se encontraron perspicacias.",
        "no_path": "No se definió el camino.",
        "no_items": "No se encontraron elementos.",
    },
    "it-IT": {
        "title": "Rapporto di Analisi Approfondita",
        "badge": "Processo di Pensiero",
        "phase_01": "Fase 01",
        "phase_02": "Fase 02",
        "phase_03": "Fase 03",
        "phase_04": "Fase 04",
        "context_label": "Il Contesto",
        "logic_label": "La Logica",
        "insight_label": "L'Intuizione",
        "path_label": "Il Percorso",
        "word_count_label": "parole",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "Basato su IA",
        "status_analyzing": "🌊 Deep Dive: Analisi del contesto e della logica...",
        "status_complete": "🌊 Deep Dive completato!",
        "notification_initiating": "🌊 Avvio del processo di pensiero Deep Dive...",
        "notification_complete": "🌊 Deep Dive completato, {user_name}! Catena di pensiero generata.",
        "error_brief": "Contenuto troppo breve ({length} caratteri). Deep Dive richiede almeno {min_length} caratteri.",
        "no_context": "Nessun contesto estratto.",
        "no_logic": "Nessuna logica decostruita.",
        "no_insight": "Nessuna intuizione trovata.",
        "no_path": "Nessun percorso definito.",
        "no_items": "Nessun elemento trovato.",
    },
    "vi-VN": {
        "title": "Báo Cáo Phân Tích Chuyên Sâu",
        "badge": "Quy Trình Tư Duy",
        "phase_01": "Giai đoạn 01",
        "phase_02": "Giai đoạn 02",
        "phase_03": "Giai đoạn 03",
        "phase_04": "Giai đoạn 04",
        "context_label": "Bối Cảnh",
        "logic_label": "Logic",
        "insight_label": "Thông Tin Chuyên Sâu",
        "path_label": "Lộ Trình",
        "word_count_label": "từ",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "Được hỗ trợ bởi AI",
        "status_analyzing": "🌊 Deep Dive: Đang phân tích bối cảnh và logic...",
        "status_complete": "🌊 Deep Dive hoàn tất!",
        "notification_initiating": "🌊 Đang khởi tạo quy trình tư duy Deep Dive...",
        "notification_complete": "🌊 Deep Dive hoàn tất, {user_name}! Chuỗi tư duy đã được tạo.",
        "error_brief": "Nội dung quá ngắn ({length} ký tự). Deep Dive cần ít nhất {min_length} ký tự.",
        "no_context": "Không có bối cảnh nào được trích xuất.",
        "no_logic": "Không có logic nào được phân tích.",
        "no_insight": "Không tìm thấy thông tin chuyên sâu nào.",
        "no_path": "Không có lộ trình nào được xác định.",
        "no_items": "Không tìm thấy mục nào.",
    },
    "id-ID": {
        "title": "Laporan Analisis Mendalam",
        "badge": "Proses Berpikir",
        "phase_01": "Fase 01",
        "phase_02": "Fase 02",
        "phase_03": "Fase 03",
        "phase_04": "Fase 04",
        "context_label": "Konteks",
        "logic_label": "Logika",
        "insight_label": "Wawasan",
        "path_label": "Jalur",
        "word_count_label": "kata",
        "footer_engine": "Deep Dive Engine v1.0",
        "footer_tag": "Didukung AI",
        "status_analyzing": "🌊 Deep Dive: Menganalisis konteks & logika...",
        "status_complete": "🌊 Deep Dive selesai!",
        "notification_initiating": "🌊 Memulai proses berpikir Deep Dive...",
        "notification_complete": "🌊 Deep Dive selesai, {user_name}! Rantai pemikiran dihasilkan.",
        "error_brief": "Konten terlalu singkat ({length} karakter). Deep Dive memerlukan setidaknya {min_length} karakter.",
        "no_context": "Tidak ada konteks yang diekstraksi.",
        "no_logic": "Tidak ada logika yang didekonstruksi.",
        "no_insight": "Tidak ada wawasan yang ditemukan.",
        "no_path": "Tidak ada jalur yang ditentukan.",
        "no_items": "Tidak ada item yang ditemukan.",
    },
}

# Supported language fallbacks
LANGUAGE_FALLBACKS = {
    "zh-HK": "zh-HK",
    "zh-TW": "zh-TW",
    "zh-MO": "zh-HK",
    "en-GB": "en-US",
    "en-AU": "en-US",
    "en-CA": "en-US",
    "es-MX": "es-ES",
    "es-AR": "es-ES",
    "fr-CA": "fr-FR",
    "fr-BE": "fr-FR",
    "fr-CH": "fr-FR",
    "de-AT": "de-DE",
    "de-CH": "de-DE",
}

PROMPTS = {
    "en-US": {
        "system": """You are a Deep Dive Analyst. Your goal is to guide the user through a comprehensive thinking process, moving from surface understanding to deep strategic action.

## Thinking Structure (STRICT)

You MUST analyze the input across these four specific dimensions:

### 1. 🔍 The Context (What?)
Provide a high-level panoramic view. What is this content about? What is the core situation, background, or problem being addressed? (2-3 paragraphs)

### 2. 🧠 The Logic (Why?)
Deconstruct the underlying structure. How is the argument built? What is the reasoning, the hidden assumptions, or the mental models at play? (Bullet points)

### 3. 💎 The Insight (So What?)
Extract the non-obvious value. What are the "Aha!" moments? What are the implications, the blind spots, or the unique perspectives revealed? (Bullet points)

### 4. 🚀 The Path (Now What?)
Define the strategic direction. What are the specific, prioritized next steps? How can this knowledge be applied immediately? (Actionable steps)

## Rules
- Output in the user's specified language.
- Maintain a professional, analytical, yet inspiring tone.
- Focus on the *process* of understanding, not just the result.
- No greetings or meta-commentary.""",
        "user": """Initiate a Deep Dive into the following content:

**User Context:**
- User: {user_name}
- Time: {current_date_time_str}
- Language: {user_language}

**Content to Analyze:**
```
{long_text_content}
```

Please execute the full thinking chain: Context → Logic → Insight → Path.""",
    },
    "zh-CN": {
        "system": """你是一位“深度下潜 (Deep Dive)”分析专家。你的目标是引导用户完成一个全面的思维过程，从表面理解深入到战略行动。

## 思维结构 (严格遵守)

你必须从以下四个维度剖析输入内容：

### 1. 🔍 The Context (全景)
提供一个高层级的全景视图。内容是关于什么的？核心情境、背景或正在解决的问题是什么？（2-3 段话）

### 2. 🧠 The Logic (脉络)
解构底层结构。论点是如何构建的？其中的推理逻辑、隐藏假设或起作用的思维模型是什么？（列表形式）

### 3. 💎 The Insight (洞察)
提取非显性的价值。有哪些“原来如此”的时刻？揭示了哪些深层含义、盲点或独特视角？（列表形式）

### 4. 🚀 The Path (路径)
定義戰略方向。具體的、按優先順位排列的下一步行動是什麼？如何立即應用這些知識？（可執行步驟）

## 規則
- 使用用戶指定的語言輸出。
- 保持專業、分析性且富有啟發性的語調。
- 聚焦於「理解的過程」，而不僅僅是結果。
- 不要包含寒暄或元對話。""",
        "user": """对以下内容发起“深度下潜”：

**用户上下文：**
- 用户：{user_name}
- 时间：{current_date_time_str}
- 语言：{user_language}

**待分析内容：**
```
{long_text_content}
```

请执行完整的思维链：全景 (Context) → 脉络 (Logic) → 洞察 (Insight) → 路径 (Path)。""",
    },
    "zh-HK": {
        "system": """你是一位「深度下潛 (Deep Dive)」分析專家。你的目標是引導用戶完成一個全面的思維過程，從表面理解深入到戰略行動。

## 思維結構 (嚴格遵守)

你必須從以下四個維度剖析輸入內容：

### 1. 🔍 The Context (全景)
提供一個高層級的全景視圖。內容是關於什麼的？核心情境、背景或正在解決的問題是什麼？（2-3 段話）

### 2. 🧠 The Logic (脈絡)
解構底層結構。論點是如何構建的？其中的推理邏輯、隱藏假設或起作用的思維模型是什麼？（列表形式）

### 3. 💎 The Insight (洞察)
提取非顯性的價值。有哪些「原來如此」的時刻？揭示了哪些深層含義、盲點或獨特視角？（列表形式）

### 4. 🚀 The Path (路徑)
定義戰略方向。具體的、按優先順位排列的下一步行動是什麼？如何立即應用這些知識？（可執行步驟）

## 規則
- 使用用戶指定的語言輸出。
- 保持專業、分析性且富有啟發性的語調。
- 聚焦於「理解的過程」，而不僅僅是結果。
- 不要包含寒暄或元對話。""",
        "user": """對以下內容發起「深度下潛」：

**用戶上下文：**
- 用戶：{user_name}
- 時間：{current_date_time_str}
- 語言：{user_language}

**待分析內容：**
```
{long_text_content}
```

請執行完整的思維鏈：全景 (Context) → 脈絡 (Logic) → 洞察 (Insight) → 路徑 (Path)。""",
    },
    "zh-TW": {
        "system": """你是一位「深度下潛 (Deep Dive)」分析專家。你的目標是引導用戶完成一個全面的思維過程，從表面理解深入到戰略行動。

## 思維結構 (嚴格遵守)

你必須從以下四個維度剖析輸入內容：

### 1. 🔍 The Context (全景)
提供一個高層級的全景視圖。內容是關於什麼的？核心情境、背景或正在解決的問題是什麼？（2-3 段話）

### 2. 🧠 The Logic (脈絡)
解構底層結構。論點是如何構建的？其中的推理邏輯、隱藏假設或起作用的思維模型是什麼？（列表形式）

### 3. 💎 The Insight (洞察)
提取非顯性的價值。有哪些「原來如此」的時刻？揭示了哪些深層含義、盲點或獨特視角？（列表形式）

### 4. 🚀 The Path (路徑)
定義戰略方向。具體的、按優先順位排列的下一步行動是什麼？如何立即應用這些知識？（可執行步驟）

## 規則
- 使用用戶指定的語言輸出。
- 保持專業、分析性且富有啟發性的語調。
- 聚焦於「理解的過程」，而不僅僅是結果。
- 不要包含寒暄或元對話。""",
        "user": """對以下內容發起「深度下潛」：

**用戶上下文：**
- 用戶：{user_name}
- 時間：{current_date_time_str}
- 語言：{user_language}

**待分析內容：**
```
{long_text_content}
```

請執行完整的思維鏈：全景 (Context) → 脈絡 (Logic) → 洞察 (Insight) → 路徑 (Path)。""",
    },
    "ja-JP": {
        "system": """あなたは「ディープダイブ (Deep Dive)」分析のエキスパートです。あなたの目標は、表面的な理解から深い戦略的行動へと、包括的な思考プロセスを通じてユーザーを導くことです。

## 思考構造 (厳守)

以下の4つの側面から入力を分析する必要があります：

### 1. 🔍 コンテキスト (The Context)
ハイレベルなパノラマビューを提供します。このコンテンツは何についてですか？中心的な状況、背景または解決されている問題は何か？（2〜3段落）

### 2. 🧠 ロジック (The Logic)
基礎となる構造を解体します。議論はどのように構築されていますか？推論、隠された仮定または働いている思考モデルは何か？（箇条書き形式）

### 3. 💎 インサイト (The Insight)
非明示的な価値を抽出します。ある「なるほど！」という瞬間はありますか？どのような深い意味、盲点または独自の視点が明らかになりましたか？（箇条書き形式）

### 4. 🚀 パス (The Path)
戦略的な方向性を定義します。具体的で優先順位付けられた次のステップは何か？この知識をすぐに適用するにはどうすればよいですか？（実行可能なステップ）

## ルール
- ユーザーが指定した言語で出力してください。
- 専門的で分析的、かつ刺激的なトーンを維持してください。
- 結果だけでなく、「理解のプロセス」に焦点を当ててください。
- 不要な挨拶やメタ対話は含めません。""",
        "user": """以下の内容に対して「ディープダイブ」を開始します：

**ユーザーコンテキスト：**
- ユーザー：{user_name}
- 日時：{current_date_time_str}
- 言語：{user_language}

**分析対象コンテンツ：**
```
{long_text_content}
```

完全な思考チェーンを実行してください：コンテキスト (Context) → ロジック (Logic) → インサイト (Insight) → パス (Path)。""",
    },
    "ko-KR": {
        "system": """귀하는 '심층 분석 (Deep Dive)' 전문가입니다. 귀하의 목표는 사용자를 표면적인 이해에서 깊은 전략적 행동으로 이끄는 포괄적인 사고 과정을 안내하는 것입니다.

## 사고 구조 (엄격 준수)

다음 네 가지 차원에서 입력을 분석해야 합니다:

### 1. 🔍 컨텍스트 (The Context)
고차원적인 파노라마 뷰를 제공합니다. 이 콘텐츠는 무엇에 관한 것입니까? 핵심 상황, 배경 또는 해결하려는 문제는 무엇입니까? (2-3문단)

### 2. 🧠 로직 (The Logic)
기저 구조를 해체합니다. 논증이 어떻게 구축되었습니까? 추론, 숨겨진 가정 또는 작용하는 사고 모델은 무엇입니까? (글머리 기호 형식)

### 3. 💎 통찰 (The Insight)
비명시적인 가치를 추출합니다. '아하!' 하는 순간은 언제입니까? 어떤 깊은 의미, 사각지대 또는 독특한 관점이 드러났습니까? (글머리 기호 형식)

### 4. 🚀 경로 (The Path)
전략적 방향을 정의합니다. 구체적이고 우선순위가 지정된 다음 단계는 무엇입니까? 이 지식을 즉시 어떻게 적용할 수 있습니까? (실행 가능한 단계)

## 규칙
- 사용자가 지정한 언어로 출력하십시오.
- 전문적이고 분석적이며 고무적인 어조를 유지하십시오.
- 결과뿐만 아니라 '이해의 과정'에 집중하십시오.
- 인사말이나 메타 대화를 포함하지 마십시오.""",
        "user": """다음 내용에 대해 '심층 분석'을 시작합니다:

**사용자 컨텍스트:**
- 사용자: {user_name}
- 시간: {current_date_time_str}
- 언어: {user_language}

**분석할 내용:**
```
{long_text_content}
```

전체 사고 체인을 실행하십시오: 컨텍스트 (Context) → 로직 (Logic) → 통찰 (Insight) → 경로 (Path).""",
    },
    "fr-FR": {
        "system": """Vous êtes un expert en « Analyse Approfondie (Deep Dive) ». Votre objectif est de guider l'utilisateur à travers un processus de réflexion complet, passant d'une compréhension superficielle à une action stratégique profonde.

## Structure de Réflexion (STRICTE)

Vous DEVEZ analyser l'entrée selon ces quatre dimensions spécifiques :

### 1. 🔍 Le Contexte (The Context)
Fournissez une vue panoramique de haut niveau. De quoi parle ce contenu ? Quelle est la situation centrale, le contexte ou le problème abordé ? (2-3 paragraphes)

### 2. 🧠 La Logique (The Logic)
Déconstruisez la structure sous-jacente. Comment l'argument est-il construit ? Quel est le raisonnement, les hypothèses cachées ou les modèles mentaux en jeu ? (Liste à puces)

### 3. 💎 L'Aperçu (The Insight)
Extrayez la valeur non explicite. Quels sont les moments « Eurêka » ? Quelles sont les implications profondes, les angles morts ou les perspectives uniques révélés ? (Liste à puces)

### 4. 🚀 Le Chemin (The Path)
Définissez la direction stratégique. Quelles sont les étapes suivantes spécifiques et priorisées ? Comment appliquer ces connaissances immédiatement ? (Étapes exploitables)

## Règles
- Produisez la réponse dans la langue spécifiée par l'utilisateur.
- Maintenez un ton professionnel, analytique et inspirant.
- Concentrez-vous sur le *processus* de compréhension, pas seulement sur le résultat.
- Pas de salutations ni de méta-commentaire.""",
        "user": """Initiez une analyse approfondie sur le contenu suivant :

**Contexte utilisateur :**
- Utilisateur : {user_name}
- Temps : {current_date_time_str}
- Langue : {user_language}

**Contenu à analyser :**
```
{long_text_content}
```

Veuillez exécuter la chaîne de réflexion complète : Contexte → Logique → Aperçu → Chemin.""",
    },
    "de-DE": {
        "system": """Sie sind ein Experte für „Tiefenanalyse (Deep Dive)“. Ihr Ziel ist es, den Benutzer durch einen umfassenden Denkprozess zu führen, der von oberflächlichem Verständnis zu tiefgreifendem strategischem Handeln führt.

## Denkstruktur (STRIKT)

Sie MÜSSEN die Eingabe in diesen vier spezifischen Dimensionen analysieren:

### 1. 🔍 Der Kontext (The Context)
Bieten Sie einen umfassenden Überblick auf hoher Ebene. Worum geht es in diesem Inhalt? Was ist die Kernsituation, der Hintergrund oder das Problem, das angegangen wird? (2-3 Absätze)

### 2. 🧠 Die Logik (The Logic)
Dekonstruieren Sie die zugrunde liegende Struktur. Wie ist das Argument aufgebaut? Was ist die Argumentation, die verborgenen Annahmen oder die wirkenden Denkmodelle? (Aufzählungspunkte)

### 3. 💎 Die Erkenntnis (The Insight)
Extrahieren Sie den nicht offensichtlichen Wert. Was sind die „Aha-Momente“? Welche tiefgreifenden Bedeutungen, blinden Flecken oder einzigartigen Perspektiven werden offenbart? (Aufzählungspunkte)

### 4. 🚀 Der Pfad (The Path)
Definieren Sie die strategische Richtung. Was sind die spezifischen, priorisierten nächsten Schritte? Wie kann dieses Wissen sofort angewendet werden? (Umsetzbare Schritte)

## Regeln
- Ausgabe in der vom Benutzer angegebenen Sprache.
- Behalten Sie einen professionellen, analytischen und dennoch inspirierenden Ton bei.
- Konzentrieren Sie sich auf den *Prozess* des Verstehens, nicht nur auf das Ergebnis.
- Keine Begrüßungen oder Meta-Kommentare.""",
        "user": """Leiten Sie eine Tiefenanalyse für den folgenden Inhalt ein:

**Benutzerkontext:**
- Benutzer: {user_name}
- Zeit: {current_date_time_str}
- Sprache: {user_language}

**Zu analysierender Inhalt:**
```
{long_text_content}
```

Bitte führen Sie die vollständige Denkkette aus: Kontext → Logik → Erkenntnis → Pfad.""",
    },
    "es-ES": {
        "system": """Usted es un experto en "Análisis Profundo (Deep Dive)". Su objetivo es guiar al usuario a través de un proceso de pensamiento integral, pasando de una comprensión superficial a una acción estratégica profunda.

## Estructura de Pensamiento (ESTRICTA)

DEBE analizar la entrada a través de estas cuatro dimensiones específicas:

### 1. 🔍 El Contexto (The Context)
Proporcione una vista panorámica de alto nivel. ¿De qué trata este contenido? ¿Cuál es la situación central, el trasfondo o el problema que se está abordando? (2-3 párrafos)

### 2. 🧠 La Lógica (The Logic)
Deconstruya la estructura subyacente. ¿Cómo se construye el argumento? ¿Cuál es el razonamiento, las suposiciones ocultas o los modelos mentales en juego? (Lista de viñetas)

### 3. 💎 La Perspicacia (The Insight)
Extraiga el valor no explícito. ¿Cuáles son los momentos de revelación? ¿Qué significados profundos, puntos ciegos o prospettive uniques se revelan? (Lista de viñetas)

### 4. 🚀 El Camino (The Path)
Defina la dirección estratégica. ¿Cuáles son los pasos a seguir específicos y priorizados? ¿Cómo se puede aplicar este conocimiento de inmediato? (Pasos accionables)

## Reglas
- Salida en el idioma especificado por el usuario.
- Mantenga un tono profesional, analítico e inspirador.
- Céntrese en el *proceso* de comprensión, no solo en el resultado.
- Sin saludos ni metacomentarios.""",
        "user": """Inicie un Análisis Profundo sobre el siguiente contenido:

**Contexto del usuario:**
- Usuario: {user_name}
- Tiempo: {current_date_time_str}
- Idioma: {user_language}

**Contenido a analizar:**
```
{long_text_content}
```

Por favor, ejecute la cadena de pensamiento completa: Contexto → Lógica → Perspicacia → Camino.""",
    },
    "it-IT": {
        "system": """Sei un esperto di "Analisi Approfondita (Deep Dive)". Il tuo obiettivo è guidare l'utente attraverso un processo di pensiero completo, passando dalla comprensione superficiale all'azione strategica profonda.

## Struttura del Pensiero (STRETTA)

DEVI analizzare l'input attraverso queste quattro dimensioni specifiche:

### 1. 🔍 Il Contesto (The Context)
Fornisci una visione panoramica di alto livello. Di cosa tratta questo contenuto? Qual è la situazione centrale, lo sfondo o il problema affrontato? (2-3 paragrafi)

### 2. 🧠 La Logica (The Logic)
Decostruisci la struttura sottostante. Come è costruito l'argomento? Qual è il ragionamento, le assunzioni nascoste o i modelli mentali in gioco? (Elenco puntato)

### 3. 💎 L'Intuizione (The Insight)
Estrai il valore non esplicito. Quali sono i momenti "Eureka"? Quali significati profondi, punti ciechi o prospettive uniche vengono rivelati? (Elenco puntato)

### 4. 🚀 Il Percorso (The Path)
Definisci la direzione strategica. Quali sono i passaggi successivi specifici e prioritari? Come applicare queste conoscenze immediatamente? (Passaggi attuabili)

## Regole
- Produci la risposta nella lingua specificata dall'utente.
- Mantieni un tono professionale, analitico e stimolante.
- Concentrati sul *processo* di comprensione, non solo sul risultato.
- Niente saluti o meta-commenti.""",
        "user": """Avvia un'Analisi Approfondita sul seguente contenuto:

**Contesto utente:**
- Utente: {user_name}
- Tempo: {current_date_time_str}
- Lingua: {user_language}

**Contenuto da analizzare:**
```
{long_text_content}
```

Esegui la catena di pensiero completa: Contesto → Logica → Intuizione → Percorso.""",
    },
    "vi-VN": {
        "system": """Bạn là chuyên gia "Phân tích chuyên sâu (Deep Dive)". Mục tiêu của bạn là hướng dẫn người dùng thực hiện một quy trình tư duy toàn diện, đi từ hiểu biết bề mặt đến hành động chiến lược sâu sắc.

## Cấu trúc tư duy (NGHIÊM NGẶT)

Bạn PHẢI phân tích đầu vào theo bốn khía cạnh cụ thể sau:

### 1. 🔍 Bối cảnh (The Context)
Cung cấp một cái nhìn toàn cảnh cấp cao. Nội dung này nói về cái gì? Tình huống cốt lõi, bối cảnh hoặc vấn đề đang được giải quyết là gì? (2-3 đoạn văn)

### 2. 🧠 Logic (The Logic)
Phân tích cấu trúc cơ bản. Lập luận được xây dựng như thế nào? Lý luận, các giả định ẩn hoặc các mô hình tư duy đang hoạt động là gì? (Danh sách dấu đầu dòng)

### 3. 💎 Thông tin chuyên sâu (The Insight)
Trích xuất giá trị không hiển nhiên. Những khoảnh khắc "Aha!" là gì? Những ý nghĩa sâu sắc, điểm mù hoặc góc nhìn độc đáo nào được tiết lộ? (Danh sách dấu đầu dòng)

### 4. 🚀 Lộ trình (The Path)
Xác định hướng đi chiến lược. Các bước tiếp theo cụ thể, được ưu tiên là gì? Làm thế nào để áp dụng kiến thức này ngay lập tức? (Các bước có thể thực hiện)

## Quy tắc
- Đầu ra bằng ngôn ngữ người dùng chỉ định.
- Duy trì giọng điệu chuyên nghiệp, phân tích nhưng vẫn đầy cảm hứng.
- Tập trung vào *quy trình* hiểu, không chỉ là kết quả.
- Không chào hỏi hoặc bình luận ngoài lề.""",
        "user": """Bắt đầu Phân tích chuyên sâu về nội dung sau:

**Bối cảnh người dùng:**
- Người dùng: {user_name}
- Thời gian: {current_date_time_str}
- Ngôn ngữ: {user_language}

**Nội dung cần phân tích:**
```
{long_text_content}
```

Vui lòng thực hiện chuỗi tư duy đầy đủ: Bối cảnh → Logic → Thông tin chuyên sâu → Lộ trình.""",
    },
    "id-ID": {
        "system": """Anda adalah seorang pakar "Analisis Mendalam (Deep Dive)". Tujuan Anda adalah membimbing pengguna melalui proses berpikir yang komprehensif, beralih dari pemahaman permukaan ke tindakan strategis yang mendalam.

## Struktur Berpikir (KETAT)

Anda HARUS menganalisis masukan melalui empat dimensi spesifik ini:

### 1. 🔍 Konteks (The Context)
Berikan pandangan panorama tingkat tinggi. Tentang apa konten ini? Apa situasi inti, latar belakang, atau masalah yang sedang ditangani? (2-3 paragraf)

### 2. 🧠 Logika (The Logic)
Dekonstruksi struktur yang mendasarinya. Bagaimana argumen dibangun? Apa penalaran, asumsi tersembunyi, atau model mental yang berperan? (Daftar poin)

### 3. 💎 Wawasan (The Insight)
Ekstrak nilai yang tidak eksplisit. Apa momen "Aha!"-nya? Makna mendalam, titik buta, atau perspektif unik apa yang terungkap? (Daftar poin)

### 4. 🚀 Jalur (The Path)
Tentukan arah strategis. Apa langkah selanjutnya yang spesifik dan diprioritaskan? Bagaimana pengetahuan ini dapat segera diterapkan? (Langkah-langkah yang dapat ditindaklanjuti)

## Aturan
- Keluaran dalam bahasa yang ditentukan pengguna.
- Pertahankan nada profesional, analitis, namun tetap inspiratif.
- Fokus pada *proses* pemahaman, bukan hanya hasilnya.
- Tanpa salam atau komentar meta.""",
        "user": """Memulai Analisis Mendalam pada konten berikut:

**Konteks Pengguna:**
- Pengguna: {user_name}
- Waktu: {current_date_time_str}
- Bahasa: Indonesian

**Konten untuk Dianalisis:**
```
{long_text_content}
```

Silakan jalankan rantai pemikiran lengkap: Konteks → Logika → Wawasan → Jalur.""",
    },
}

# =================================================================
# Premium CSS Design - Deep Dive Theme
# =================================================================

CSS_TEMPLATE = """
        .deep-dive {
            font-family: 'Inter', -apple-system, system-ui, sans-serif;
            color: var(--dd-text-secondary);
        }

        .dd-header {
            background: var(--dd-header-gradient);
            padding: 40px 32px;
            color: white;
            position: relative;
        }

        .dd-header-badge {
            display: inline-block;
            padding: 4px 12px;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            border-radius: 100px;
            font-size: 0.75rem;
            font-weight: 600;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            margin-bottom: 16px;
        }

        .dd-title {
            font-size: 2rem;
            font-weight: 800;
            margin: 0 0 12px 0;
            letter-spacing: -0.02em;
        }

        .dd-meta {
            display: flex;
            gap: 20px;
            font-size: 0.85rem;
            opacity: 0.7;
        }

        .dd-body {
            padding: 32px;
            display: flex;
            flex-direction: column;
            gap: 40px;
            position: relative;
            background: var(--dd-bg-primary);
        }

        /* The Thinking Line */
        .dd-body::before {
            content: '';
            position: absolute;
            left: 52px;
            top: 40px;
            bottom: 40px;
            width: 2px;
            background: var(--dd-border);
            z-index: 0;
        }

        .dd-step {
            position: relative;
            z-index: 1;
            display: flex;
            gap: 24px;
        }

        .dd-step-icon {
            flex-shrink: 0;
            width: 40px;
            height: 40px;
            background: var(--dd-bg-primary);
            border: 2px solid var(--dd-border);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.25rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.03);
            transition: all 0.3s ease;
        }

        .dd-step:hover .dd-step-icon {
            border-color: var(--dd-accent);
            transform: scale(1.1);
        }

        .dd-step-content {
            flex: 1;
        }

        .dd-step-label {
            font-size: 0.75rem;
            font-weight: 700;
            color: var(--dd-accent);
            text-transform: uppercase;
            letter-spacing: 0.1em;
            margin-bottom: 4px;
        }

        .dd-step-title {
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--dd-text-primary);
            margin: 0 0 16px 0;
        }

        .dd-text {
            line-height: 1.7;
            font-size: 1rem;
        }

        .dd-text p { margin-bottom: 16px; }
        .dd-text p:last-child { margin-bottom: 0; }

        .dd-list {
            list-style: none;
            padding: 0;
            margin: 0;
            display: grid;
            gap: 12px;
        }

        .dd-list-item {
            background: var(--dd-bg-secondary);
            padding: 16px 20px;
            border-radius: 12px;
            border-left: 4px solid var(--dd-border);
            transition: all 0.2s ease;
        }

        .dd-list-item:hover {
            background: var(--dd-bg-tertiary);
            border-left-color: var(--dd-accent);
            transform: translateX(4px);
        }

        .dd-list-item strong {
            color: var(--dd-text-primary);
            display: block;
            margin-bottom: 4px;
        }

        .dd-path-item {
            background: var(--dd-accent-soft);
            border-left-color: var(--dd-accent);
        }

        .dd-footer {
            padding: 24px 32px;
            background: var(--dd-bg-secondary);
            border-top: 1px solid var(--dd-border);
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--dd-text-dim);
        }

        .dd-tag {
            padding: 2px 8px;
            background: var(--dd-bg-tertiary);
            border-radius: 4px;
            font-weight: 600;
        }

        .dd-text code,
        .dd-list-item code {
            background: var(--dd-code-bg);
            color: var(--dd-text-primary);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'SF Mono', 'Consolas', 'Monaco', monospace;
            font-size: 0.85em;
        }

        .dd-list-item em {
            font-style: italic;
            color: var(--dd-text-dim);
        }
"""

CONTENT_TEMPLATE = """
        <div class="deep-dive">
            <div class="dd-header">
                <div class="dd-header-badge">{{badge}}</div>
                <h1 class="dd-title">{{title}}</h1>
                <div class="dd-meta">
                    <span>👤 {user_name}</span>
                    <span>📅 {current_date_time_str}</span>
                    <span>📊 {word_count} {{word_count_label}}</span>
                </div>
            </div>
            <div class="dd-body">
                <!-- Step 1: Context -->
                <div class="dd-step">
                    <div class="dd-step-icon">🔍</div>
                    <div class="dd-step-content">
                        <div class="dd-step-label">{{phase_01}}</div>
                        <h2 class="dd-step-title">{{context_label}}</h2>
                        <div class="dd-text">{context_html}</div>
                    </div>
                </div>

                <!-- Step 2: Logic -->
                <div class="dd-step">
                    <div class="dd-step-icon">🧠</div>
                    <div class="dd-step-content">
                        <div class="dd-step-label">{{phase_02}}</div>
                        <h2 class="dd-step-title">{{logic_label}}</h2>
                        <div class="dd-text">{logic_html}</div>
                    </div>
                </div>

                <!-- Step 3: Insight -->
                <div class="dd-step">
                    <div class="dd-step-icon">💎</div>
                    <div class="dd-step-content">
                        <div class="dd-step-label">{{phase_03}}</div>
                        <h2 class="dd-step-title">{{insight_label}}</h2>
                        <div class="dd-text">{insight_html}</div>
                    </div>
                </div>

                <!-- Step 4: Path -->
                <div class="dd-step">
                    <div class="dd-step-icon">🚀</div>
                    <div class="dd-step-content">
                        <div class="dd-step-label">{{phase_04}}</div>
                        <h2 class="dd-step-title">{{path_label}}</h2>
                        <div class="dd-text">{path_html}</div>
                    </div>
                </div>
            </div>
            <div class="dd-footer">
                <span>{{footer_engine}}</span>
                <span><span class="dd-tag">{{footer_tag}}</span></span>
            </div>
        </div>
"""


class Action:
    class Valves(BaseModel):
        SHOW_STATUS: bool = Field(
            default=True,
            description="Whether to show operation status updates.",
        )
        SHOW_DEBUG_LOG: bool = Field(
            default=False,
            description="Whether to print debug logs in the browser console.",
        )
        MODEL_ID: str = Field(
            default="",
            description="LLM Model ID for analysis. Empty = use current model.",
        )
        MIN_TEXT_LENGTH: int = Field(
            default=200,
            description="Minimum text length for deep dive (chars).",
        )
        CLEAR_PREVIOUS_HTML: bool = Field(
            default=True,
            description="Whether to clear previous plugin results.",
        )
        MESSAGE_COUNT: int = Field(
            default=1,
            description="Number of recent messages to analyze.",
        )

    def __init__(self):
        self.valves = self.Valves()

    def _resolve_language(self, language: str) -> str:
        """Resolves language code to supported translation keys."""
        if language in TRANSLATIONS:
            return language
        return LANGUAGE_FALLBACKS.get(language, "en-US")

    def _get_translation(self, language: str) -> Dict[str, str]:
        """Gets the translation dictionary for the given language."""
        lang_key = self._resolve_language(language)
        return TRANSLATIONS.get(lang_key, TRANSLATIONS["en-US"])

    def _get_prompt(self, language: str, prompt_type: str) -> str:
        """Gets the prompt for the given language and type."""
        lang_key = self._resolve_language(language)
        if lang_key not in PROMPTS:
            lang_key = "en-US"
        return PROMPTS[lang_key][prompt_type]

    async def _get_user_context(
        self,
        __user__: Optional[Dict[str, Any]],
        __event_call__: Optional[Callable[[Any], Awaitable[None]]] = None,
        __request__: Optional[Request] = None,
    ) -> Dict[str, str]:
        """Safely extracts user context information."""
        if isinstance(__user__, (list, tuple)):
            user_data = __user__[0] if __user__ else {}
        elif isinstance(__user__, dict):
            user_data = __user__
        else:
            user_data = {}

        user_id = user_data.get("id", "unknown_user")
        user_name = user_data.get("name", "User")
        # Default from profile
        user_language = user_data.get("language", "en-US")

        # Level 1 Fallback: Accept-Language from __request__ headers
        if (
            __request__
            and hasattr(__request__, "headers")
            and "accept-language" in __request__.headers
        ):
            raw_lang = __request__.headers.get("accept-language", "")
            if raw_lang:
                user_language = raw_lang.split(",")[0].split(";")[0]

        # Priority: Document Lang > LocalStorage (Frontend) > Browser > Request Header > Profile
        if __event_call__:
            try:
                js_code = """
                    try {
                        return (
                            document.documentElement.lang ||
                            localStorage.getItem('locale') || 
                            localStorage.getItem('language') || 
                            navigator.language || 
                            'en-US'
                        );
                    } catch (e) {
                        return 'en-US';
                    }
                """
                # Use asyncio.wait_for to prevent hanging if frontend fails to callback
                frontend_lang = await asyncio.wait_for(
                    __event_call__({"type": "execute", "data": {"code": js_code}}),
                    timeout=2.0,
                )
                if frontend_lang and isinstance(frontend_lang, str):
                    user_language = frontend_lang
            except Exception as e:
                logger.warning(f"Failed to retrieve frontend language: {e}")

        return {
            "user_id": user_id,
            "user_name": user_name,
            "user_language": user_language,
        }

    def _get_chat_context(
        self, body: dict, __metadata__: Optional[dict] = None
    ) -> Dict[str, str]:
        """
        Unified extraction of chat context information (chat_id, message_id).
        Prioritizes extraction from body, then metadata.
        """
        chat_id = ""
        message_id = ""

        # 1. Try to get from body
        if isinstance(body, dict):
            chat_id = body.get("chat_id", "")
            message_id = body.get("id", "")  # message_id is usually 'id' in body

            # Check body.metadata as fallback
            if not chat_id or not message_id:
                body_metadata = body.get("metadata", {})
                if isinstance(body_metadata, dict):
                    if not chat_id:
                        chat_id = body_metadata.get("chat_id", "")
                    if not message_id:
                        message_id = body_metadata.get("message_id", "")

        # 2. Try to get from __metadata__ (as supplement)
        if __metadata__ and isinstance(__metadata__, dict):
            if not chat_id:
                chat_id = __metadata__.get("chat_id", "")
            if not message_id:
                message_id = __metadata__.get("message_id", "")

        return {
            "chat_id": str(chat_id).strip(),
            "message_id": str(message_id).strip(),
        }

    def _process_llm_output(self, llm_output: str) -> Dict[str, str]:
        """Parse LLM output and convert to styled HTML."""
        # Extract sections using flexible regex (supports English and Chinese keywords)
        context_match = re.search(
            r"###\s*1\.\s*🔍?\s*(?:The Context|全景)\s*(?:\(.*\))?\s*\n(.*?)(?=\n###|$)",
            llm_output,
            re.DOTALL | re.IGNORECASE,
        )
        logic_match = re.search(
            r"###\s*2\.\s*🧠?\s*(?:The Logic|脉络)\s*(?:\(.*\))?\s*\n(.*?)(?=\n###|$)",
            llm_output,
            re.DOTALL | re.IGNORECASE,
        )
        insight_match = re.search(
            r"###\s*3\.\s*💎?\s*(?:The Insight|洞察)\s*(?:\(.*\))?\s*\n(.*?)(?=\n###|$)",
            llm_output,
            re.DOTALL | re.IGNORECASE,
        )
        path_match = re.search(
            r"###\s*4\.\s*🚀?\s*(?:The Path|路径)\s*(?:\(.*\))?\s*\n(.*?)(?=\n###|$)",
            llm_output,
            re.DOTALL | re.IGNORECASE,
        )

        # Fallback if numbering is different
        if not context_match:
            context_match = re.search(
                r"###\s*🔍?\s*(?:The Context|全景).*?\n(.*?)(?=\n###|$)",
                llm_output,
                re.DOTALL | re.IGNORECASE,
            )
        if not logic_match:
            logic_match = re.search(
                r"###\s*🧠?\s*(?:The Logic|脉络).*?\n(.*?)(?=\n###|$)",
                llm_output,
                re.DOTALL | re.IGNORECASE,
            )
        if not insight_match:
            insight_match = re.search(
                r"###\s*💎?\s*(?:The Insight|洞察).*?\n(.*?)(?=\n###|$)",
                llm_output,
                re.DOTALL | re.IGNORECASE,
            )
        if not path_match:
            path_match = re.search(
                r"###\s*🚀?\s*(?:The Path|路径).*?\n(.*?)(?=\n###|$)",
                llm_output,
                re.DOTALL | re.IGNORECASE,
            )

        context_md = (
            context_match.group(1 if context_match.lastindex == 1 else 2).strip()
            if context_match
            else ""
        )
        logic_md = (
            logic_match.group(1 if logic_match.lastindex == 1 else 2).strip()
            if logic_match
            else ""
        )
        insight_md = (
            insight_match.group(1 if insight_match.lastindex == 1 else 2).strip()
            if insight_match
            else ""
        )
        path_md = (
            path_match.group(1 if path_match.lastindex == 1 else 2).strip()
            if path_match
            else ""
        )

        if not any([context_md, logic_md, insight_md, path_md]):
            context_md = llm_output.strip()
            logger.warning("LLM output did not follow format. Using as context.")

        md_extensions = ["nl2br"]

        context_html = (
            markdown.markdown(context_md, extensions=md_extensions)
            if context_md
            else ""
        )
        logic_html = (
            self._process_list_items(logic_md, "logic") if logic_md else ""
        )
        insight_html = (
            self._process_list_items(insight_md, "insight") if insight_md else ""
        )
        path_html = (
            self._process_list_items(path_md, "path") if path_md else ""
        )

        return {
            "context_html": context_html,
            "logic_html": logic_html,
            "insight_html": insight_html,
            "path_html": path_html,
        }

    def _process_list_items(self, md_content: str, section_type: str) -> str:
        """Convert markdown list to styled HTML cards with full markdown support."""
        lines = md_content.strip().split("\n")
        items = []
        current_paragraph = []

        for line in lines:
            line = line.strip()

            # Check for list item (bullet or numbered)
            bullet_match = re.match(r"^[-*]\s+(.+)$", line)
            numbered_match = re.match(r"^\d+\.\s+(.+)$", line)

            if bullet_match or numbered_match:
                # Flush any accumulated paragraph
                if current_paragraph:
                    para_text = " ".join(current_paragraph)
                    para_html = self._convert_inline_markdown(para_text)
                    items.append(f"<p>{para_html}</p>")
                    current_paragraph = []

                # Extract the list item content
                text = (
                    bullet_match.group(1) if bullet_match else numbered_match.group(1)
                )

                # Handle bold title pattern: **Title:** Description or **Title**: Description
                title_match = re.match(r"\*\*(.+?)\*\*[:\s]*(.*)$", text)
                if title_match:
                    title = self._convert_inline_markdown(title_match.group(1))
                    desc = self._convert_inline_markdown(title_match.group(2).strip())
                    path_class = "dd-path-item" if section_type == "path" else ""
                    item_html = f'<div class="dd-list-item {path_class}"><strong>{title}</strong>{desc}</div>'
                else:
                    text_html = self._convert_inline_markdown(text)
                    path_class = "dd-path-item" if section_type == "path" else ""
                    item_html = (
                        f'<div class="dd-list-item {path_class}">{text_html}</div>'
                    )
                items.append(item_html)
            elif line and not line.startswith("#"):
                # Accumulate paragraph text
                current_paragraph.append(line)
            elif not line and current_paragraph:
                # Empty line ends paragraph
                para_text = " ".join(current_paragraph)
                para_html = self._convert_inline_markdown(para_text)
                items.append(f"<p>{para_html}</p>")
                current_paragraph = []

        # Flush remaining paragraph
        if current_paragraph:
            para_text = " ".join(current_paragraph)
            para_html = self._convert_inline_markdown(para_text)
            items.append(f"<p>{para_html}</p>")

        if items:
            return f'<div class="dd-list">{" ".join(items)}</div>'
        return f'<p class="dd-no-content">No items found.</p>'

    def _convert_inline_markdown(self, text: str) -> str:
        """Convert inline markdown (bold, italic, code) to HTML."""
        # Convert inline code: `code` -> <code>code</code>
        text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
        # Convert bold: **text** -> <strong>text</strong>
        text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
        # Convert italic: *text* -> <em>text</em> (but not inside **)
        text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
        return text

    async def _emit_status(
        self,
        emitter: Optional[Callable[[Any], Awaitable[None]]],
        description: str,
        done: bool = False,
    ):
        """Emits a status update event."""
        if self.valves.SHOW_STATUS and emitter:
            await emitter(
                {"type": "status", "data": {"description": description, "done": done}}
            )

    async def _emit_notification(
        self,
        emitter: Optional[Callable[[Any], Awaitable[None]]],
        content: str,
        ntype: str = "info",
    ):
        """Emits a notification event."""
        if emitter:
            await emitter(
                {"type": "notification", "data": {"type": ntype, "content": content}}
            )

    async def _emit_debug_log(self, emitter, title: str, data: dict):
        """Print structured debug logs in the browser console"""
        if not self.valves.SHOW_DEBUG_LOG or not emitter:
            return

        try:
            import json

            js_code = f"""
                (async function() {{
                    console.group("🛠️ {title}");
                    console.log({json.dumps(data, ensure_ascii=False)});
                    console.groupEnd();
                }})();
            """

            await emitter({"type": "execute", "data": {"code": js_code}})
        except Exception as e:
            print(f"Error emitting debug log: {e}")

    def _remove_existing_html(self, content: str) -> str:
        """Removes existing plugin-generated HTML."""
        pattern = r"```html\s*<!-- OPENWEBUI_PLUGIN_OUTPUT -->[\s\S]*?```"
        return re.sub(pattern, "", content).strip()

    def _extract_text_content(self, content) -> str:
        """Extract text from message content."""
        if isinstance(content, str):
            return content
        elif isinstance(content, list):
            text_parts = []
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    text_parts.append(item.get("text", ""))
                elif isinstance(item, str):
                    text_parts.append(item)
            return "\n".join(text_parts)
        return str(content) if content else ""

    def _merge_html(
        self,
        existing_html: str,
        new_content: str,
        new_styles: str = "",
        user_language: str = "en-US",
    ) -> str:
        """Merges new content into HTML container."""
        if "<!-- OPENWEBUI_PLUGIN_OUTPUT -->" in existing_html:
            base_html = re.sub(r"^```html\s*", "", existing_html)
            base_html = re.sub(r"\s*```$", "", base_html)
        else:
            base_html = HTML_WRAPPER_TEMPLATE.replace("{user_language}", user_language)

        wrapped = f'<div class="plugin-item">\n{new_content}\n</div>'

        if new_styles:
            base_html = base_html.replace(
                "/* STYLES_INSERTION_POINT */",
                f"{new_styles}\n/* STYLES_INSERTION_POINT */",
            )

        base_html = base_html.replace(
            "<!-- CONTENT_INSERTION_POINT -->",
            f"{wrapped}\n<!-- CONTENT_INSERTION_POINT -->",
        )

        return base_html.strip()

    def _build_content_html(self, context: dict, i18n: dict) -> str:
        """Build content HTML."""
        html = CONTENT_TEMPLATE
        # Fill i18n placeholders
        for key, value in i18n.items():
            html = html.replace(f"{{{{{key}}}}}", str(value))

        # Fill data placeholders
        for key, value in context.items():
            if value == "":
                fallback_key = f"no_{key.replace('_html', '')}"
                value = f'<p class="dd-no-content">{i18n.get(fallback_key, "")}</p>'
            html = html.replace(f"{{{key}}}", str(value))
        return html

    async def action(
        self,
        body: dict,
        __user__: Optional[Dict[str, Any]] = None,
        __event_emitter__: Optional[Callable[[Any], Awaitable[None]]] = None,
        __event_call__: Optional[Callable[[Any], Awaitable[None]]] = None,
        __request__: Optional[Request] = None,
    ) -> Optional[dict]:
        logger.info("Action: Deep Dive v1.0.0 started")

        user_ctx = await self._get_user_context(
            __user__, __event_call__, __request__
        )
        user_id = user_ctx["user_id"]
        user_name = user_ctx["user_name"]
        user_language = user_ctx["user_language"]
        i18n = self._get_translation(user_language)

        now = datetime.now()
        current_date_time_str = now.strftime("%b %d, %Y %H:%M")

        original_content = ""
        try:
            messages = body.get("messages", [])
            if not messages:
                raise ValueError("No messages found.")

            message_count = min(self.valves.MESSAGE_COUNT, len(messages))
            recent_messages = messages[-message_count:]

            aggregated_parts = []
            for msg in recent_messages:
                text = self._extract_text_content(msg.get("content"))
                if text:
                    aggregated_parts.append(text)

            if not aggregated_parts:
                raise ValueError("No text content found.")

            original_content = "\n\n---\n\n".join(aggregated_parts)
            word_count = len(original_content.split())

            if len(original_content) < self.valves.MIN_TEXT_LENGTH:
                msg = i18n["error_brief"].format(
                    length=len(original_content),
                    min_length=self.valves.MIN_TEXT_LENGTH,
                )
                await self._emit_notification(__event_emitter__, msg, "warning")
                return {"messages": [{"role": "assistant", "content": f"⚠️ {msg}"}]}

            await self._emit_notification(
                __event_emitter__, i18n["notification_initiating"], "info"
            )
            await self._emit_status(
                __event_emitter__, i18n["status_analyzing"], False
            )

            prompt = self._get_prompt(user_language, "user").format(
                user_name=user_name,
                current_date_time_str=current_date_time_str,
                user_language=user_language,
                long_text_content=original_content,
            )

            model = self.valves.MODEL_ID or body.get("model")
            payload = {
                "model": model,
                "messages": [
                    {
                        "role": "system",
                        "content": self._get_prompt(user_language, "system"),
                    },
                    {"role": "user", "content": prompt},
                ],
                "stream": False,
            }

            user_obj = await _call_db(Users.get_user_by_id, user_id)
            if not user_obj:
                raise ValueError(f"User not found: {user_id}")

            response = await generate_chat_completion(__request__, payload, user_obj)
            llm_output = response["choices"][0]["message"]["content"]

            processed = self._process_llm_output(llm_output)

            context = {
                "user_name": user_name,
                "current_date_time_str": current_date_time_str,
                "word_count": word_count,
                **processed,
            }

            content_html = self._build_content_html(context, i18n)

            # Handle existing HTML
            existing = ""
            match = re.search(
                r"```html\s*(<!-- OPENWEBUI_PLUGIN_OUTPUT -->[\s\S]*?)```",
                original_content,
            )
            if match:
                existing = match.group(1)

            if self.valves.CLEAR_PREVIOUS_HTML or not existing:
                original_content = self._remove_existing_html(original_content)
                final_html = self._merge_html(
                    "", content_html, CSS_TEMPLATE, user_language
                )
            else:
                original_content = self._remove_existing_html(original_content)
                final_html = self._merge_html(
                    existing, content_html, CSS_TEMPLATE, user_language
                )

            body["messages"][-1][
                "content"
            ] = f"{original_content}\n\n```html\n{final_html}\n```"

            await self._emit_status(__event_emitter__, i18n["status_complete"], True)
            await self._emit_notification(
                __event_emitter__,
                i18n["notification_complete"].format(user_name=user_name),
                "success",
            )

        except Exception as e:
            logger.error(f"Deep Dive Error: {e}", exc_info=True)
            body["messages"][-1][
                "content"
            ] = f"{original_content}\n\n❌ **Error:** {str(e)}"
            await self._emit_status(__event_emitter__, "Deep Dive failed.", True)
            await self._emit_notification(
                __event_emitter__, f"Error: {str(e)}", "error"
            )

        return body
