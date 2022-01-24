#mcandrew;

PYTHON:=python3 -W ignore

COMMITprefix:=Forecasts generated for LUcompUncertLab-VAR2 model on
COMMITsuffix:=$(shell date +"%Y-%m-%d")

COMMIT:=$(COMMITprefix) $(COMMITsuffix)

runall: collectAndFormatData generateForecasts postprocess checkLocations plotTrajectories zip sync
.PHONY: runall

collectAndFormatData:
	$(PYTHON) LUcompUncertLab-dataprep.py && echo "data prepared"

generateForecasts:
	$(PYTHON) LUcompUncertLab-VAR2.py && echo "forecasts generated"

postprocess:
	$(PYTHON) LUcompUncertLab-postProcess.py && echo "Post process complete"

checkLocations:
	$(PYTHON) checkFile.py && echo "Location information"

plotTrajectories:
	$(PYTHON) plotTrajectories.py && echo "Plotted trajectories"

add:
	git add .

commit:
	git commit -m "$(COMMIT)"

push:
	git push

zip:
	gzip *allPredictions.csv

send: add commit push
.PHONY: send

sync:
	rsync -arvz --progress ../LUcompUncertLab-VAR2/ ../../../2022FluSightModels/LUcompUncertLab-VAR2 && \
	make -C ../../../2022FluSightModels/
