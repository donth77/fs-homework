import sys, json
from collections import defaultdict, deque

SEPARATOR = '#'
ROUTE_STR = 'route'
ROOT_STR = '/'
NOTFOUND_STR = '404'
WILDCARD_STR = 'X'
PATH_STR = 'path'
STATIC_STR = 'static'

# tree is a dict whose default values are trees
def tree(): return defaultdict(tree)

routeDict = {}
routes = tree()
# create root of routes tree
routes[ROOT_STR]
config = True
 
for line in open('./input2.txt','r').readlines(): 
  lineStr = line.split()

  if lineStr[0] == SEPARATOR:
      config = False
  if config:
      routeDict[lineStr[0]] = lineStr[1]
      routeComponents = lineStr[0].split(ROOT_STR)[1:]
      if routeComponents[0] == '':
          routes[ROOT_STR][ROUTE_STR] = lineStr[1]
      else:
          currLevel = routes[ROOT_STR]
          for component in routeComponents:
              currLevel = currLevel[component]
          currLevel[ROUTE_STR] = lineStr[1]

  elif lineStr[0] != SEPARATOR:
      reqPathComponents = lineStr[0].split(ROOT_STR)[1:]
      
      if reqPathComponents[0] == '':
          print(routes[ROOT_STR][ROUTE_STR]) if ROUTE_STR in routes[ROOT_STR] else print(NOTFOUND_STR)
      else:
          #print('========================================================')
          #print(reqPathComponents)
          currLevelPaths = [{PATH_STR: routes[ROOT_STR], STATIC_STR : True}]
          #print(json.dumps(currLevelPaths))
          num = 1
          for component in reqPathComponents:
              if not currLevelPaths: break
              #print('--------------/')
              #print(f'level {i}')5
              #component = reqPathComponents[i]
              #print(f'component: {component}')
              #print(len(currLevelPaths))
              nextLevelPaths = []
              for pathDict in currLevelPaths:
                  route = pathDict[PATH_STR]
                  #print('--------------//')
                  #print(json.dumps(route))
                  if component in route:
                      #print('found component')
                      num += 1
                      nextLevelPaths.append({PATH_STR : route[component], STATIC_STR : pathDict[STATIC_STR]})
                  if WILDCARD_STR in route:
                      #print('found wildcard')
                      num += 1
                      nextLevelPaths.append({PATH_STR : route[WILDCARD_STR], STATIC_STR : False})
              currLevelPaths = nextLevelPaths
              #print(len(currLevelPaths))
          #print(json.dumps(currLevelPaths))
          #print(json.dumps(currLevelPaths[0]))
          #print(json.dumps(currLevelPaths[1]))
          #print(json.dumps(currLevelPaths[2]))
          print(lineStr[0])
          print('num: ' , num)
          print('comp len: ',len(reqPathComponents))
          if currLevelPaths:
              hasStaticPath = False
              for pathDict in currLevelPaths:
                  if pathDict[STATIC_STR]:
                      hasStaticPath = True
                      print(pathDict[PATH_STR][ROUTE_STR])
                      break
              if not hasStaticPath:
                  print(currLevelPaths[0][PATH_STR][ROUTE_STR])
          else:
              print(NOTFOUND_STR)
          print()
          #print(currLevelPaths[0][ROUTE_STR]) if currLevelPaths else print(NOTFOUND_STR)
                  


