import sys
import argparse
import cv2
import numpy as np
from scipy.spatial import distance as dist
import matplotlib.pyplot as plt

imagePath1 = 'SoftwareHardware_Simpson.jpg'
imagePath2 = 'bannerminimundi1.jpg'
imagePath3 = 'INSPIRELogo_Ok.png'
image1 = cv2.imread(imagePath1)
image2 = cv2.imread(imagePath2)
colorImage1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
colorImage2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
print(type(image1), image1.shape, image1[:5, :5, 0])
print(type(colorImage2), colorImage2.shape, colorImage2[:5, :5, 0])
hist1 = cv2.calcHist([image1], [0, 1, 2], None, [8, 8, 8],
        [0, 256, 0, 256, 0, 256])
hist2 = cv2.calcHist([image2], [0, 1, 2], None, [8, 8, 8],
        [0, 256, 0, 256, 0, 256])
hist3 = cv2.calcHist([image2], [0], None, [8],
        [0, 255])
print('hist1', type(hist1), hist1.shape, hist1[:5, :5, 0])
print('hist2', type(hist2), hist2.shape, hist2[:5, :5, 0])
print('hist3', type(hist3), hist3.shape, hist3[:, 0])
print('hist3', type(hist3), hist3.shape, hist3[:, 0]/np.sum(hist3))
hist1n = cv2.normalize(hist1, hist1).flatten()
hist2n = cv2.normalize(hist2, hist2).flatten()
hist3n = cv2.normalize(hist3, hist3).flatten()
print('hist1n', type(hist1n), hist1n.shape, hist1n[:20])
print('hist2n', type(hist2n), hist2n.shape, hist2n[:20])
print('hist3n', type(hist3n), hist3n.shape, hist3n[:20])


OPENCV_METHODS = (
    ("Correlation", cv2.HISTCMP_CORREL),
    ("Chi-Squared", cv2.HISTCMP_CHISQR),
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))
# loop over the comparison methods
for (methodName, method) in OPENCV_METHODS:
    # initialize the results dictionary and the sort
    # direction
    results = {}
    reverse = False
    # if we are using the correlation or intersection
    # method, then sort the results in reverse order
    if methodName in ("Correlation", "Intersection"):
        reverse = True

    # compute the distance between the two histograms
    # using the method and update the results dictionary
    d = cv2.compareHist(hist1n, hist2n, method)
    print(methodName, d)
    # results[0] = d
    # # sort the results
    # results = sorted([(v, k) for (k, v) in results.items()], reverse = reverse)
    
    # # show the query image
    # fig = plt.figure("Query")
    # ax = fig.add_subplot(1, 1, 1)
    # # ax.imshow(imagePath3)
    # plt.axis("off")
    # # initialize the results figure
    # fig = plt.figure("Results: %s" % (methodName))
    # fig.suptitle(methodName, fontsize = 20)

    # # loop over the results
    # for (i, (v, k)) in enumerate(results):
        # # show the result
        # ax = fig.add_subplot(1, 1, i + 1)
        # ax.set_title("%s: %.2f" % (k, v))
        # # plt.imshow(imagePath1)
        # plt.axis("off")
# # show the OpenCV methods
# plt.show()

print('\nScipy')
SCIPY_METHODS = (
    ("Euclidean", dist.euclidean),
    ("Manhattan", dist.cityblock),
    ("Chebysev", dist.chebyshev))
# loop over the comparison methods
for (methodName, method) in SCIPY_METHODS:
    # initialize the dictionary dictionary
    results = {}
    # loop over the index
    d = method(hist1n, hist2n)
    print(methodName, d)

quit()

print('\npruebas-> importando qlidtwins...')
from cartolidar import qlidtwins
print('\npruebas-> importando DasoLidarSource...')
from cartolidar.clidtools.clidtwins import DasoLidarSource

print('\npruebas-> Probando leerConfiguracion()...')
listaVerbose = ['', '-v', '-vv', '-vvv']
for verboses in listaVerbose:
    print('\tverboses', verboses)
    if verboses != '':
        if sys.argv[-1] in listaVerbose:
            sys.argv.pop()
        sys.argv.append(verboses)
    print('pruebas-> sys.argv:', sys.argv)
    # listaInputs = [True,]
    # monkeypatch.setattr('builtins.input', lambda _: listaInputs.pop(0))
    argsConfig = qlidtwins.leerConfiguracion()
    assert type(argsConfig) == argparse.Namespace, 'La funcion debe devolver un objeto de la clase <class "argparse.Namespace">.'
    assert len(argsConfig.__dict__) > 0, 'Deberia haber algun argumento en linea de comandos.'
    print('\ntest_leerArgumentos ok')
    cfgDict = qlidtwins.creaConfigDict(argsConfig)
    myDasolidar = qlidtwins.clidtwinsUseCase(cfgDict, accionPral=0)
    print('test_qlidtwins-> searchSourceFiles')
    # assert len(myDasolidar.inFilesListAllTypes) == 2, 'El match de ejemplo debe encontrar 2 ficheros asc con variables dasoLidar'
    assert len(myDasolidar.inFilesListAllTypes) == 3, 'El match de ejemplo debe encontrar 3 tipos de fichero asc con variables dasoLidar'
    assert len(myDasolidar.inFilesListAllTypes[0]) == 2, 'El match de ejemplo debe encontrar 2 ficheros asc de cada tipo con variables dasoLidar'
    print('\ntest_UseCase_0 ok')

quit()

print('\npruebas-> Instanciando DasoLidarSource...')
myDasolidar = DasoLidarSource(LCL_verbose=2)

print('\npruebas-> Buscando ficheros...')
# mylistaTxtDasoVarsFileTypes = 'FccRptoAmdk_PrimeRets_0025_0150,FccRptoAmdk_TodosRets_200cm_50%HD,MFE25,TMasa'
mylistaTxtDasoVarsFileTypes = 'Alt95,Fcc05,Fcc03'
mylistaTxtDasoVarsFileTypes = 'CeldasAlt95SobreMdk,FccRptoAmdk_PrimeRets_MasDe0500,FccRptoAmdk_PrimeRets_MasDe0300'
myDasolidar.searchSourceFiles(
    LCL_listaTxtDasoVarsFileTypes=mylistaTxtDasoVarsFileTypes,
    LCL_rutaAscRaizBase='O:/Sigmena/usuarios/COMUNES/Bengoa/Lidar/cartoLidar/Sg_PinoSilvestre',
)

print('\npruebas-> Creando un fichero raster (Tiff) que integra todas las variables dasoLidar...')
myDasolidar.createMultiDasoLayerRasterFile(
    LCL_rutaCompletaMFE='O:/Sigmena/Carto/VEGETACI/MFE/MFE50/MFE50AD/40_MFE50AD_etrs89.shp',
    LCL_cartoMFEcampoSp='SP1',
)

print('\npruebas-> Analizando el fichero raster (Tiff) creado con todas las variables dasoLidar...')
myDasolidar.analyzeMultiDasoLayerRasterFile(
    LCL_patronVectrName='O:/Sigmena/usuarios/COMUNES/Bengoa/Lidar/cartoLidar/Sg_PinoSilvestre/poligonos Riaza1.shp',
    LCL_patronLayerName='',
)

print('\npruebas-> Generando zonas similares...')
myDasolidar.generarRasterCluster()

print('\npruebas-> Fin.')