"""
oldymbols: Provide the old symbols (old Python API, for PDFreactor 7),
but pointing to the new values.

For migration / conversion purposes only;
our export profiles are still based on the old API.

We are *not* interested in

- the actual (usually numeric) values of those old symbols
- inventing old-looking symbols for new functionality.

For the transformation of old API method calls to config variable assignments,
see ./oldmethods.py
"""

# Python compatibility:
from __future__ import absolute_import, print_function

# from pdfreactor.api import PDFreactor as _new

OLD2NEW = {

    # Cleanup: perform a cleanup when loading a document ...[
    'CLEANUP_NONE':	'Cleanup.NONE',	# no cleanup
    'CLEANUP_JTIDY':	'Cleanup.JTIDY',	# use JTidy
    'CLEANUP_CYBERNEKO':	'Cleanup.CYBERNEKO',	# use the CyberNeko HTML parser
    'CLEANUP_TAGSOUP':	'Cleanup.TAGSOUP',	# use the TagSoup HTML parser
    'CLEANUP_DEFAULT':	'Cleanup.CYBERNEKO',

    # ] Document type constants ... [

    'DOCTYPE_AUTODETECT':	'Doctype.AUTODETECT',
    'DOCTYPE_XML':	'Doctype.XML',
    'DOCTYPE_XHTML':	'Doctype.XHTML',
    'DOCTYPE_HTML5':	'Doctype.HTML5',
    'DOCTYPE_DEFAULT':	'Doctype.AUTODETECT',

    # ] Document default language constant ... [
    # NO SUCH SYMBOL in the new Python API, right?!
    'DOCUMENT_DEFAULT_LANGUAGE_DEFAULT': None,

    # ] Encryption constants ... [
    'ENCRYPTION_NONE':	'Encryption.NONE',
    'ENCRYPTION_40':	'Encryption.TYPE_40',  # 40 bit encryption
    'ENCRYPTION_128':	'Encryption.TYPE_128', # 128 bit encryption
    'ENCRYPTION_DEFAULT':	'Encryption.NONE',

    # ] Log level constants ... [
    # (old API method: setLogLevel(int)
    'LOG_LEVEL_NONE':	'LogLevel.NONE',
    'LOG_LEVEL_FATAL':	'LogLevel.FATAL',
    'LOG_LEVEL_WARN':	'LogLevel.WARN',
    'LOG_LEVEL_INFO':	'LogLevel.INFO',
    'LOG_LEVEL_DEBUG':	'LogLevel.DEBUG',
    'LOG_LEVEL_PERFORMANCE':	'LogLevel.PERFORMANCE',
    'LOG_LEVEL_DEFAULT':	'LogLevel.NONE',

    # ] Viewerpreferences ... [
    # (old API method: setViewerPreferences(int)
    'VIEWER_PREFERENCES_PAGE_LAYOUT_SINGLE_PAGE':	'ViewerPreferences.PAGE_LAYOUT_SINGLE_PAGE',
    'VIEWER_PREFERENCES_PAGE_LAYOUT_ONE_COLUMN':	'ViewerPreferences.PAGE_LAYOUT_ONE_COLUMN',
    'VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_COLUMN_LEFT':	'ViewerPreferences.PAGE_LAYOUT_TWO_COLUMN_LEFT',
    'VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_COLUMN_RIGHT':	'ViewerPreferences.PAGE_LAYOUT_TWO_COLUMN_RIGHT',
    'VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_PAGE_LEFT':	'ViewerPreferences.PAGE_LAYOUT_TWO_PAGE_LEFT',
    'VIEWER_PREFERENCES_PAGE_LAYOUT_TWO_PAGE_RIGHT':	'ViewerPreferences.PAGE_LAYOUT_TWO_PAGE_RIGHT',
    'VIEWER_PREFERENCES_PAGE_MODE_USE_NONE':	'ViewerPreferences.PAGE_MODE_USE_NONE',
    'VIEWER_PREFERENCES_PAGE_MODE_USE_OUTLINES':	'ViewerPreferences.PAGE_MODE_USE_OUTLINES',
    'VIEWER_PREFERENCES_PAGE_MODE_USE_THUMBS':	'ViewerPreferences.PAGE_MODE_USE_THUMBS',
    'VIEWER_PREFERENCES_PAGE_MODE_FULLSCREEN':	'ViewerPreferences.PAGE_MODE_FULLSCREEN',
    'VIEWER_PREFERENCES_PAGE_MODE_USE_OC':	'ViewerPreferences.PAGE_MODE_USE_OC',
    'VIEWER_PREFERENCES_PAGE_MODE_USE_ATTACHMENTS':	'ViewerPreferences.PAGE_MODE_USE_ATTACHMENTS',
    'VIEWER_PREFERENCES_HIDE_TOOLBAR':	'ViewerPreferences.HIDE_TOOLBAR',
    'VIEWER_PREFERENCES_HIDE_MENUBAR':	'ViewerPreferences.HIDE_MENUBAR',
    'VIEWER_PREFERENCES_HIDE_WINDOW_UI':	'ViewerPreferences.HIDE_WINDOW_UI',
    'VIEWER_PREFERENCES_FIT_WINDOW':	'ViewerPreferences.FIT_WINDOW',
    'VIEWER_PREFERENCES_CENTER_WINDOW':	'ViewerPreferences.CENTER_WINDOW',
    'VIEWER_PREFERENCES_DISPLAY_DOC_TITLE':	'ViewerPreferences.DISPLAY_DOC_TITLE',
    'VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_NONE':	'ViewerPreferences.NON_FULLSCREEN_PAGE_MODE_USE_NONE',
    'VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_OUTLINES':	'ViewerPreferences.NON_FULLSCREEN_PAGE_MODE_USE_OUTLINES',
    'VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_THUMBS':	'ViewerPreferences.NON_FULLSCREEN_PAGE_MODE_USE_THUMBS',
    'VIEWER_PREFERENCES_NON_FULLSCREEN_PAGE_MODE_USE_OC':	'ViewerPreferences.NON_FULLSCREEN_PAGE_MODE_USE_OC',
    'VIEWER_PREFERENCES_DIRECTION_L2R':	'ViewerPreferences.DIRECTION_L2R',
    'VIEWER_PREFERENCES_DIRECTION_R2L':	'ViewerPreferences.DIRECTION_R2L',
    'VIEWER_PREFERENCES_PRINTSCALING_NONE':	'ViewerPreferences.PRINTSCALING_NONE',
    'VIEWER_PREFERENCES_PRINTSCALING_APPDEFAULT':	'ViewerPreferences.PRINTSCALING_APPDEFAULT',
    'VIEWER_PREFERENCES_DUPLEX_SIMPLEX':	'ViewerPreferences.DUPLEX_SIMPLEX',
    'VIEWER_PREFERENCES_DUPLEX_FLIP_SHORT_EDGE':	'ViewerPreferences.DUPLEX_FLIP_SHORT_EDGE',
    'VIEWER_PREFERENCES_DUPLEX_FLIP_LONG_EDGE':	'ViewerPreferences.DUPLEX_FLIP_LONG_EDGE',
    'VIEWER_PREFERENCES_PICKTRAYBYPDFSIZE_FALSE':	'ViewerPreferences.PICKTRAYBYPDFSIZE_FALSE',
    'VIEWER_PREFERENCES_PICKTRAYBYPDFSIZE_TRUE':	'ViewerPreferences.PICKTRAYBYPDFSIZE_TRUE',

    'COLOR_SPACE_RGB':	'ColorSpace.RGB',
    'COLOR_SPACE_CMYK':	'ColorSpace.CMYK',

    # ] Conformance constants ... [
    # (old API method: setConformance(int)
    'CONFORMANCE_PDF':	'Conformance.PDF',
    'CONFORMANCE_PDFA1A':	'Conformance.PDFA1A',
    'CONFORMANCE_PDFA3A':	'Conformance.PDFA3A',
    'CONFORMANCE_PDFA':	'Conformance.PDFA3A',
    'CONFORMANCE_DEFAULT':	'Conformance.PDF',

    # ] Processing Preferences Constants ... [

    'PROCESSING_PREFERENCES_SAVE_MEMORY_IMAGES':	'ProcessingPreferences.SAVE_MEMORY_IMAGES',

    # ] Exceeding Content Constants ... [
    # (old API method: setLogExceedingContent(int, int)
    'EXCEEDING_CONTENT_ANALYZE_NONE':	'ExceedingContentAnalyze.NONE',
    'EXCEEDING_CONTENT_ANALYZE_CONTENT':	'ExceedingContentAnalyze.CONTENT',
    'EXCEEDING_CONTENT_ANALYZE_CONTENT_AND_STATIC_BOXES':	'ExceedingContentAnalyze.CONTENT_AND_STATIC_BOXES',
    'EXCEEDING_CONTENT_ANALYZE_CONTENT_AND_BOXES':	'ExceedingContentAnalyze.CONTENT_AND_BOXES',
    'EXCEEDING_CONTENT_AGAINST_NONE':	'ExceedingContentAgainst.NONE',
    'EXCEEDING_CONTENT_AGAINST_PAGE_BORDERS':	'ExceedingContentAgainst.PAGE_BORDERS',
    'EXCEEDING_CONTENT_AGAINST_PAGE_CONTENT':	'ExceedingContentAgainst.PAGE_CONTENT',
    'EXCEEDING_CONTENT_AGAINST_PARENT':	'ExceedingContentAgainst.PARENT',

    # ] Overlay & Merge Constants ... [
    # (old API method: setMergeMode(int)
    'MERGE_MODE_APPEND':	'MergeMode.APPEND',
    'MERGE_MODE_PREPEND':	'MergeMode.PREPEND',
    'MERGE_MODE_OVERLAY':	'MergeMode.OVERLAY',
    'MERGE_MODE_OVERLAY_BELOW':	'MergeMode.OVERLAY_BELOW',
    # (old API method: setOverlayRepeat(int)
    'OVERLAY_REPEAT_NONE':	'OverlayRepeat.NONE',
    'OVERLAY_REPEAT_LAST_PAGE':	'OverlayRepeat.LAST_PAGE',
    'OVERLAY_REPEAT_ALL_PAGES':	'OverlayRepeat.ALL_PAGES',

    # ] Multipage & Order Constants ... [
    # (old API method: setPagesPerSheetProperties(int)
    'PAGES_PER_SHEET_DIRECTION_RIGHT_DOWN':	'PagesPerSheetDirection.RIGHT_DOWN',
    'PAGES_PER_SHEET_DIRECTION_LEFT_DOWN':	'PagesPerSheetDirection.LEFT_DOWN',
    'PAGES_PER_SHEET_DIRECTION_RIGHT_UP':	'PagesPerSheetDirection.RIGHT_UP',
    'PAGES_PER_SHEET_DIRECTION_LEFT_UP':	'PagesPerSheetDirection.LEFT_UP',
    'PAGES_PER_SHEET_DIRECTION_DOWN_RIGHT':	'PagesPerSheetDirection.DOWN_RIGHT',
    'PAGES_PER_SHEET_DIRECTION_DOWN_LEFT':	'PagesPerSheetDirection.DOWN_LEFT',
    'PAGES_PER_SHEET_DIRECTION_UP_RIGHT':	'PagesPerSheetDirection.UP_RIGHT',
    'PAGES_PER_SHEET_DIRECTION_UP_LEFT':	'PagesPerSheetDirection.UP_LEFT',
    # (old API method: setPageOrder(string)
    'PAGE_ORDER_REVERSE':	'PageOrder.REVERSE',
    'PAGE_ORDER_ODD':	'PageOrder.ODD',
    'PAGE_ORDER_EVEN':	'PageOrder.EVEN',
    'PAGE_ORDER_BOOKLET':	'PageOrder.BOOKLET',
    'PAGE_ORDER_BOOKLET_RTL':	'PageOrder.BOOKLET_RTL',

    # ] Signing mode Constants ... [
    'KEYSTORE_TYPE_PKCS12':	'KeystoreType.PKCS12',
    'KEYSTORE_TYPE_JKS':	'KeystoreType.JKS',
    'SIGNING_MODE_SELF_SIGNED':	'SigningMode.SELF_SIGNED',
    'SIGNING_MODE_VERISIGN_SIGNED':	'SigningMode.VERISIGN_SIGNED',
    'SIGNING_MODE_WINCER_SIGNED':	'SigningMode.WINCER_SIGNED',

    # ] JavaScript mode Constants ... [
    # (old API method: setJavaScriptMode(int)
    'JAVASCRIPT_MODE_DISABLED':	'JavaScriptMode.DISABLED',
    'JAVASCRIPT_MODE_ENABLED':	'JavaScriptMode.ENABLED',
    'JAVASCRIPT_MODE_ENABLED_NO_LAYOUT':	'JavaScriptMode.ENABLED_NO_LAYOUT',
    'JAVASCRIPT_MODE_ENABLED_REAL_TIME':	'JavaScriptMode.ENABLED_REAL_TIME',
    'JAVASCRIPT_MODE_ENABLED_TIME_LAPSE':	'JavaScriptMode.ENABLED_TIME_LAPSE',
    'JAVASCRIPT_MODE_DEFAULT':	'JavaScriptMode.DISABLED',

    # ] HTTPS mode Constants ... [
    # (old API method: setHttpsMode(int)
    'HTTPS_MODE_STRICT':	'HttpsMode.STRICT',
    'HTTPS_MODE_LENIENT':	'HttpsMode.LENIENT',
    'HTTPS_MODE_DEFAULT':	'HttpsMode.STRICT',

    # ] Output Format Constants ... [
    # (old API method: setOutputFormat(int, int, int)
    'OUTPUT_FORMAT_PDF':	'OutputType.PDF',
    'OUTPUT_FORMAT_JPEG':	'OutputType.JPEG',
    'OUTPUT_FORMAT_PNG':	'OutputType.PNG',
    'OUTPUT_FORMAT_PNG_TRANSPARENT':	'OutputType.PNG_TRANSPARENT',
    'OUTPUT_FORMAT_BMP':	'OutputType.BMP',
    'OUTPUT_FORMAT_GIF':	'OutputType.GIF',
    'OUTPUT_FORMAT_PNG_AI':	'OutputType.PNG_AI',
    'OUTPUT_FORMAT_PNG_TRANSPARENT_AI':	'OutputType.PNG_TRANSPARENT_AI',
    'OUTPUT_FORMAT_TIFF_LZW':	'OutputType.TIFF_LZW',
    'OUTPUT_FORMAT_TIFF_PACKBITS':	'OutputType.TIFF_PACKBITS',
    'OUTPUT_FORMAT_TIFF_UNCOMPRESSED':	'OutputType.TIFF_UNCOMPRESSED',
    'OUTPUT_FORMAT_TIFF_CCITT_1D':	'OutputType.TIFF_CCITT_1D',
    'OUTPUT_FORMAT_TIFF_CCITT_GROUP_3':	'OutputType.TIFF_CCITT_GROUP_3',
    'OUTPUT_FORMAT_TIFF_CCITT_GROUP_4':	'OutputType.TIFF_CCITT_GROUP_4',
    }


if __name__ == '__main__':
    # Standard library:
    from pprint import pprint
    # Local imports:
    from pdfreactor.parsecfg.symbols import SYMBOL_STRINGS as _new

    removed = set()
    found_new = set()
    for key, val in OLD2NEW.items():
        if val is None:
            removed.add(key)
            continue
        found_new.add(val)
        dic = {
            'Old symbol': key,
            'New symbol': val,
            'New value': _new[val],
        }
        pprint(dic)
    print('%d symbols have been removed:' % len(removed))
    print(sorted(removed))
    print('%d symbols have new names:' % len(found_new))
    print(sorted(found_new))
    new_only = set(_new) - found_new
    print('%d symbols have been added:' % len(new_only))
    print(sorted(new_only))

