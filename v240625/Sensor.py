import machine
import onewire
import ds18x20
import dht
import sys
if sys.platform!='win32':import uasyncio as asyncio
else:import asyncio
class Sensor:
	def __init__(self,app):self._app=app;ds_pin=machine.Pin(13);self.ds_sensor=ds18x20.DS18X20(onewire.OneWire(ds_pin));self.sensor=dht.DHT11(machine.Pin(12));self.roms=self.ds_sensor.scan();print('Found DS devices: ',self.roms);asyncio.get_event_loop().create_task(self.run())
	async def run(self):
		await asyncio.sleep(20)
		while True:
			try:self.sensor.measure();await asyncio.sleep_ms(100);temp=self.sensor.temperature();hum=self.sensor.humidity();temp_f=temp*(9/5)+32.;self._app.info['Temp']=temp;self._app.info['Hum']=hum
			except OSError as e:self._app.info['Temp']=-100;self._app.info['Hum']=-100
			try:
				if not self.roms:self.roms=self.ds_sensor.scan();await asyncio.sleep_ms(100)
				self.ds_sensor.convert_temp();await asyncio.sleep_ms(750)
				try:
					id_=1
					for rom in self.roms:
						temp_rom=self.ds_sensor.read_temp(rom);temp_rom=int(temp_rom/.25)*.25
						if id_<3:self._app.info['Temp'+str(id_)]=temp_rom
						id_+=1
				except:self._app.info['Temp1']=-100;self._app.info['Temp2']=-100;self.roms=self.ds_sensor.scan()
			except:self.roms=self.ds_sensor.scan()
			await asyncio.sleep(5)
