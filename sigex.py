from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import os
import platform

executables = {
	'chromedriver': {
		'Windows': ['chromedriver.exe', 'C:\\'],
		'Darwin': ['chromedriver', '/usr/']
	},
	'google_chrome': {
		'Windows': ['chrome.exe', 'C:\\'],
		'Darwin': ['Google Chrome', '/Applications/']
	}
}

def wait(sec):
	time.sleep(sec)

def find_path_of(target, possible_path):
	for root, dirs, files in os.walk(rf'{possible_path}'):
		for name in files:
			if name == target:
				return os.path.abspath(os.path.join(root, name))

def options():
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	if platform.system() == 'Windows':
		options.add_experimental_option('excludeSwitches', ['enable-logging'])
	options.add_experimental_option("excludeSwitches", ['enable-automation'])
	program, path = executables['google_chrome'][platform.system()]
	options.binary_location = find_path_of(program, path)
	return options

def chrome_driver_binary():
	program, path = executables['chromedriver'][platform.system()]
	return find_path_of(program, path)

def download_file(dir_name, link):
	options = webdriver.ChromeOptions()
	options.add_argument('--start-maximized')
	options.add_experimental_option("prefs", {"download.default_directory" : dir_name})
	driver = webdriver.Chrome(chrome_driver_binary(), options = options)
	driver.get(link)
	driver.maximize_window()
	wait(5)

	rar_file_links = WebDriverWait(driver, 8).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'td a:not([href="/SIGEX_2019/"])')))
	# Descargo los archivos de los proyectos separados por carpeta
	for rar in rar_file_links:
		file_name = rar.get_attribute('href').split("/")[-1]
		current_path = dir_name + "/" + file_name
		# Descargar el archivo solo si no se descargó antes
		if not os.path.isfile(current_path):
			rar.click()
			# Esperar a que se descargue el archivo para descargar el siguiente
			while not os.path.isfile(current_path):
				wait(1)
		else:
			print(f"Archivo {file_name} ya descargado")
	driver.quit()

def download_files_from_links():
	print("> Descargando archivos de SIGEX")
	for link in links:
		current_dir_name = base_dir + link.split("https://portalgeo.sernageomin.cl/SIGEX_2019/")[-1]
		if (os.path.isdir(current_dir_name) and ignore_dirs) or not os.path.isdir(current_dir_name):
			download_file(current_dir_name, link)

def get_sigex_links():
	print("> Obteniendo links de SIGEX desde:")
	sigex_url = 'https://sernageomin.maps.arcgis.com/apps/dashboards/f47a3c43bb974de486313d2f15e70fda'
	print(sigex_url)
	# Configuro usar Chrome como navegador
	driver = webdriver.Chrome(chrome_driver_binary(), options = options())

  # Selectores CSS (para encontrar elementos en una página web)
	details_css_selector = "body > div.full-page-container.bg-background > calcite-shell > div.dashboard-container.shadow-2.relative.calcite-mode-dark.flex.flex-auto.flex-col.overflow-hidden > div.flex-auto.flex.relative.overflow-hidden > div > div > div > margin-container > full-container > div:nth-child(20) > margin-container > full-container > div > div > div:nth-child(3) > div"
	num_of_projects_css_selector = "body > div.full-page-container.bg-background > calcite-shell > div.dashboard-container.shadow-2.relative.calcite-mode-dark.flex.flex-auto.flex-col.overflow-hidden > div.flex-auto.flex.relative.overflow-hidden > div > div > div > margin-container > full-container > div:nth-child(11) > margin-container > full-container > dashboard-tab-zone > div > div.collection-pagination.mx-1.text-center.flex.justify-center > div.flex-none.btn-label.self-center"
	link_css_selector_container = ".feature-widget.esri-feature.esri-widget a"
	project_name_css_selector = "body > div.full-page-container.bg-background > calcite-shell > div.dashboard-container.shadow-2.relative.calcite-mode-dark.flex.flex-auto.flex-col.overflow-hidden > div.flex-auto.flex.relative.overflow-hidden > div > div > div > margin-container > full-container > div:nth-child(11) > margin-container > full-container > dashboard-tab-zone > div > div.widget-body.flex-auto.w-full.flex.flex-col.overflow-y-auto.overflow-x-hidden > div > div > div > div > div > div > table > tbody > tr:nth-child(1) > td"
	right_arrow_css_selector = ".collection-pagination calcite-action[title='Entidad siguiente']"

  # Abro una ventana con la página de SIGEX
	driver.get(sigex_url)
	driver.maximize_window()

  # Hago clic en la pestaña de Detalles
	WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, details_css_selector))).click()
	wait(5)
	num_of_projects = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, num_of_projects_css_selector))).text.split('1 de ')[-1]
	wait(5)
	i = 0
	while i < int(num_of_projects):
		project_name = ""
		try:
			project_name = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, project_name_css_selector))).text
			# Trato de obtener el link si existe
			url = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, link_css_selector_container))).get_attribute('href')
			print(f"> {i+1}. Link obtenido de {project_name}: {url}")
			# Agregar link solo si no está presente
			if url not in links:
				links.append(url)
		except Exception as e:
			print(f"> {i+1}. ERROR: No se pudo obtener el link de {project_name}")
		# Hago clic en la flecha para ver el siguiente proyecto
		WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.CSS_SELECTOR, right_arrow_css_selector))).click()
		i += 1
	# Cierro la ventana de SIGEX
	driver.close()

def create_file_with_links():
	print("> Creando archivo sigex_links.txt con links")
	# Crear (abrir) archivo
	f = open('sigex_links.txt' , 'w')
	# Llenarlo con los links
	for link in links:
		f.write(link + "\n")
	# Cerrar archivo
	f.close()

def read_links_from_file():
	print("> Leyendo links desde archivo sigex_links.txt")
	with open('sigex_links.txt') as f:
		for line in f:
			links.append(line.strip())

def ask_user_for_input():
	print("")
	print("¿Quieres obtener links de la página de SIGEX?")
	print("    > Ingresa 1 para obtenerlos")
	print("    > Ingresa otro caracter para descargar los datos en base a sigex_links.txt")
	print("")
	print("    ** Apreta la tecla Enter después de ingresar el caracter escogido")
	print("")
	input("Respuesta: (1/cualquier otro caracter)")

if __name__ == "__main__":
	global links
	global ignore_dirs
	global base_dir
	links = []
	# Si es False, no descargará archivos si la carpeta ya existe
	# Cambiar por True para revisar si faltan archivos por descargar en carpetas ya existentes
	ignore_dirs = False
	# Directorio en donde se descargaran los archivos
	base_dir = "/Users/fjvalles/Downloads/"
	option = ask_user_for_input()
	if option == 1:
		get_sigex_links()
		wait(5)
		create_file_with_links()
		wait(5)
	read_links_from_file()
	download_files_from_links()