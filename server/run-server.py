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
        params = web.input( method='sync', rules="A=0", fullt="1", steps="10" )
        
        try:
            message = None
            steps   = min( [ 100, abs(int(params.steps)) ] )
            fullt   = min( [  10, abs(int(params.fullt)) ] )
            assert params.method in "sync async lpde".split()
        except Exception, exc:
            message = str(exc)
        
    
        print render.results( message=message, params=params )

class index:
    "Main index"
    def GET(self ):
        print render.index()

web.webapi.internalerror = web.debugerror

if __name__ == "__main__": 
    web.run(urls, globals(), web.reloader)