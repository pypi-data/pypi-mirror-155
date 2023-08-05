# CGC Client - K8s Cloud

cgc command line client for k8s Comtegra cloud environment.
Installation: `pip install cgcsdk`

# Backend

`http://172.16.246.2:21919/docs`

# To implement

- cgc volume
  - create `<name>*` --size* <int GB> --type <HDD|SSD*> --access <RWO|RWX\*>
  - delete --name\*
  - list
- cgc compute
  - create `<entity>` --gpu <int max 8> --cpu <int cores> --memory <int GB> --volume <string name> --name <string name>
  - delete `<entity>` --name <string name>
  - list
  - stop `<entity>` --name <string name> - brak endpointa na backendzie
- cgc billing - status rachunku. Aplikacja nalicza sekundowo za zużyte zasoby. Rachunek w formie faktury na koniec miesiąca rozliczeniowego. Jeśli payAsYouGo, trzeba podłączyć blokowanie środków na karcie. Jeśli zasilane saldo, trzeba zadbać o odpowiednie mechanizmy informujące o wyczerpaniu zasobów.
  - status
  - fvat ls id - wylistuj lub otwórz fakturę o danym ID
  - pay - interfejs do łatwego płacenia, uruchamia w przeglądarce sesje PayU. Trzeba zadbać o CLI
- cgc status - podstawowe komendy do monitorowania uruchomionych kontenerów.
  - ps
  - `<id | name>` - odpowiednik docker inspect
  - inspect `<id | name>`
- cgc rm `<id | name>` - usuwa kontener
  - f --force, wyłącza i usuwa kontener, pozostawia podpięte volumeny.
- cgc stop `<name>` - zatrzymuje kontener - stop nie zatrzymuje naliczania zużycia zasobów ponieważ karta jest nadal przypisana do kontenera w tym użytkownika. Możemy naliczać w formie rezerwacji, mniejsza kwota, brak zużycia prądu.

# Developer guide

To write documentation for this project you need to install plugin for auto doc-stringing.  
`autoDocstring - Python Docstring Generator`  
Then change in settings of the plugin `@ext:njpwerner.autodocstring` docsstringing format to **Sphinx**

## Install for python at current selected version

`& C:/Users/jzboina/AppData/Local/Microsoft/WindowsApps/python3.9.exe -m pip install -U black`

## Build and publish new version on PyPI
- **Generate distribution packages**
  - install latest build version: `pip install --upgrade build`
  - from the root project directory run `pythom -m build`
  - once completed it should generate a `dist` directory with two files in it
- **Upload the distribution archives**
  - install latest twine version: `pip install --upgrade twine`
  - upload both files in `dist` directory: `python -m twine upload dist/*`
  - enter your username and password for PyPi
  - new version should be visible at [PyPI](https://pypi.org/project/cgcsdk/)