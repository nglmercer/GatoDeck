from obswebsocket import obsws, requests
import asyncio
import json

class API_OBS:
    def __init__(self) -> None:
        self.connection = False
        self.client = None

    def connect_to_obs(self, host: str, port: int, password: str) -> None:
        """
        Connect to OBS using the provided host, port, and password.
        """
        try:
            self.client = obsws(host=host, port=port, password=password)
            self.client.connect()
            self.connection = True
        except Exception as e:
            print('Error al conectar a OBS:', e)

    def get_version(self):
        data = self.client.call(requests.GetVersion())
        myJson = {
            'name': data.name,
            'availableRequests': data.datain['availableRequests'],
            'obsVersion': data.datain['obsVersion'],
            'obsWebSocketVersion': data.datain['obsWebSocketVersion'],
            'platform': data.datain['platform'],
            'platformDescription': data.datain['platformDescription'],
            'rpcVersion': data.datain['rpcVersion'],
            'supportedImageFormats': data.datain['supportedImageFormats']
        }
        return myJson

    def get_scene_list(self):
        esceneversion = self.client.call(requests.GetSceneList())

        return esceneversion

    def get_GetStats(self):
        dataStats = self.client.call(requests.GetStats())
        myJson2 = {
                'name': dataStats.name,
                'activeFps': dataStats.datain['activeFps'],
                'availableDiskSpace': dataStats.datain['availableDiskSpace'],
                'averageFrameRenderTime': dataStats.datain['averageFrameRenderTime'],
                'cpuUsage': dataStats.datain['cpuUsage'],
                'memoryUsage': dataStats.datain['memoryUsage'],
                'outputSkippedFrames': dataStats.datain['outputSkippedFrames'],
                'outputTotalFrames': dataStats.datain['outputTotalFrames'],
                'renderSkippedFrames': dataStats.datain['renderSkippedFrames'],
                'renderTotalFrames': dataStats.datain['renderTotalFrames'],
                'webSocketSessionIncomingMessages': dataStats.datain['webSocketSessionIncomingMessages'],
                'webSocketSessionOutgoingMessages': dataStats.datain['webSocketSessionOutgoingMessages'],
                'dataout': dataStats.dataout,
                'status': dataStats.status
            }
        return myJson2

    def get_data1(self):
        try:
            stat1 = self.get_version()
            json_data1 = json.dumps(stat1)
            return json_data1
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            return None

    def get_data3(self):
        try:
            state3 = self.get_GetStats()
            json_data3 = json.dumps(state3)
            return json_data3
        except Exception as e:
            print(f"Error al obtener los datos3: {e}")
            return None

    def get_data2(self):
        try:
            stat2 = self.get_scene_list()
            json_data2 = json.dumps(stat2)
            return json_data2
        except Exception as e:
            print(f"Error al obtener los datos: {e}")
            return None

    def get_obs_version(self):
        '''
        Obtiene la version actual de OBS
        '''
        if self.connection == False:
            try:
                self.client.reconnect()
            except Exception as e:
                return f'Hubo un error: {e}'
        if self.connection:
            return f'Version actual: {self.client.call(requests.GetVersion()).getObsVersion()}'
        else:
            return 'Desconectado de obs | Soporte para Api V5'

    def get_list_obs_scenes(self):
        '''
        Obtiene la lista de escenas disponibles en OBS.
        ```
        def get_list_obs_scenes(): -> Dict and Str in console
        ```
        '''
        if self.connection == False:
            try:
                self.client.reconnect()
            except Exception as e:
                return 'Error al obtener la lista de escenas'
        if self.connection:
            # Obtener la losta de escenas
            try:
                scenes = self.client.call(requests.GetSceneList())
                # print(vars(scenes))
                print(type(scenes))
                print(f"Escena actual: {scenes.datain['currentProgramSceneName']},\nLista de escenas: {scenes.datain['scenes']},\n Estatus: {scenes.status}")
                return scenes.datain['scenes']
            except Exception as e:
                print(f'error {e}')
                return 'Error al obtener la lista de escenas.'

    def set_scenne(self, name: str):
        '''
        Hay que pasarle el nombre de la escena a usar.
        '''
        self.client.call(requests.SetCurrentProgramScene(sceneName=name))
        print(f'Ejecutando funcion de cambiar escena {name}')

    def stream(self, action: str):
        '''
        Resibe una accion la cual para prender o apagar stream.
        ```
        def stream(action):
            if action == 'stream-on':
                client.call(requests.StartStream())
                return f'Accion: {action}'
            elif action == 'stream-off':
                client.call(requests.StopStream())
                return f'Accion: {action}'
        ```
        '''
        if action == 'stream-on':
            self.client.call(requests.StartStream())
            return f'Accion: {action}'
        elif action == 'stream-off':
            self.client.call(requests.StopStream())
            return f'Accion: {action}'

    def record(self, action: str):
        '''
        Resibe una accion la cual para prender o apagar grabacion.
        ```
        def record(action):
            if action == 'record-on':
                client.call(requests.StartRecord())
                return f'Accion: {action}'
            elif action == 'record-off':
                client.call(requests.StopRecord())
                return f'Accion: {action}'
        ```
        '''
        if action == 'record-on':
            self.client.call(requests.StartRecord())
            return f'Accion: {action}'
        elif action == 'record-off':
            self.client.call(requests.StopRecord())
            return f'Accion: {action}'
        elif action == 'record-toggle-pause':
            self.client.call(requests.ToggleRecordPause())

apiObs = API_OBS()

