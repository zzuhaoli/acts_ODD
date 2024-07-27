#!/usr/bin/env python3
from pathlib import Path

import acts
import acts.examples
from acts.examples.simulation import addParticleGun, addFatras, EtaConfig,MomentumConfig
from acts.examples import GenericDetector, AlignedDetector, TGeoDetector

u = acts.UnitConstants


def runFatras(trackingGeometry, field, outputDir, s: acts.examples.Sequencer = None):
    s = s or acts.examples.Sequencer(events=1000, numThreads=-1)
    s.config.logLevel = acts.logging.WARNING
    rnd = acts.examples.RandomNumbers()
    addParticleGun(
        s,
        EtaConfig(-4, 4),
        MomentumConfig(1,10),
        rnd=rnd,
    )
    outputDir = Path(outputDir)
    addFatras(
        s,
        trackingGeometry,
        field,
        outputDirCsv=outputDir / "csv",
        outputDirRoot=outputDir,
        rnd=rnd,
        #logLevel = acts.logging.VERBOSE
    )
    return s


if "__main__" == __name__:
    matDeco = None
    #matDeco = acts.IMaterialDecorator.fromFile("geometry-map.json")

    logLevel=acts.logging.VERBOSE
    customLogLevel = acts.examples.defaultLogging(logLevel=logLevel)

    jsonFile=Path.cwd() / "tgeo_ODD_v01_config.json"
    tgeo_fileName=Path.cwd() / "DD4hep_ODD_DC.root"
    (
        detector,
        trackingGeometry,
        decorators,
    ) = TGeoDetector.create(
            jsonFile=str(jsonFile),
            fileName=str(tgeo_fileName),
            surfaceLogLevel=customLogLevel(),
            layerLogLevel=customLogLevel(),
            volumeLogLevel=customLogLevel(),
            mdecorator=matDeco,
    )

    field = acts.ConstantBField(acts.Vector3(0, 0, 2 * u.T))

    runFatras(trackingGeometry, field, Path.cwd()).run()
