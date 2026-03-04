import traceback, sys
print('Python', sys.version)
try:
    import weasyprint
    print('weasyprint', getattr(weasyprint, '__version__', 'unknown'))
except Exception:
    print('ERROR importing weasyprint:')
    traceback.print_exc()
try:
    import cairo
    print('cairo import OK')
except Exception:
    print('ERROR importing cairo:')
    traceback.print_exc()
try:
    import cairocffi
    print('cairocffi import OK', getattr(cairocffi, '__version__', 'unknown'))
except Exception:
    print('ERROR importing cairocffi:')
    traceback.print_exc()
try:
    from weasyprint import HTML
    HTML(string='<p>hola</p>').write_pdf('prueba_weasy.pdf')
    print('PDF written: prueba_weasy.pdf')
except Exception:
    print('ERROR generating PDF:')
    traceback.print_exc()
print('done')
