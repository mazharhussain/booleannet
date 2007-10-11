import sys
# add
sys.path.extend( [ '..', 'web.zip'] )

import web
import boolean
import pylab

urls = (
  '/', 'index',
  '/simulate', 'simulate' 
  
)

render = web.template.render('static/', cache=False )

class simulate:
    "Simulation results"
    def POST(self ):
        print render.results()

class index:
    "Main index"
    def GET(self ):
        print render.index()

web.webapi.internalerror = web.debugerror

if __name__ == "__main__": 
    web.run(urls, globals(), web.reloader)