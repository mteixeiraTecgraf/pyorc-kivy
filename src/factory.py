

from mockDevController import MockDevController
from devcontroller import DeviceController
from application import Application

from kivy.app import App
class Root:
    pass

def deviceController(provider):
    from android import AnderoidController
    return AnderoidController(provider.get(Root))

android = False

class Factory:
    def __init__(self):
        self.provider = Provider()
        self.provider.addSingleton(Application,Application,[DeviceController, App])
            #self.provider.addSingletonFunc(DeviceController,deviceController)
        if(android):
            self.provider.addSingletonFunc(DeviceController,deviceController)
        else:
            self.provider.addSingleton(DeviceController,MockDevController,[Root])
    
def createSingletonFunc(Class, Deps):
    
    def func(provider):
        def getDep(dep):
            return provider.get(dep)
        return Class(*map(getDep, Deps))
    return func
class Provider():
    def __init__(self):
        self.singletons={}
        self.instances={}

    def addSingletonFunc(self, BaseC, Func):
        self.singletons[BaseC]=Func
        
    def addSingleton(self, BaseC, Class, deps):
        self.addSingletonFunc(BaseC, createSingletonFunc(Class, deps))

    def addSingletonInstance(self, BaseC, instance):
        self.instances[BaseC]=instance
            
    def get(self, Class):
        if(self.instances.get(Class)):
            return self.instances[Class]
        self.addSingletonInstance(Class,self.singletons[Class](self))

        return self.instances[Class]