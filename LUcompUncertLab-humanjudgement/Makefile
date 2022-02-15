#mcandrew;

PYTHON:=python3 -W ignore

COMMITprefix:=Forecasts generated for LUcompUncertLab-humanjudgement model on
COMMITsuffix:=$(shell date +"%Y-%m-%d")

COMMIT:=$(COMMITprefix) $(COMMITsuffix)

runall: collectAndFormatData interpolate generateForecasts postprocess plotTrajectories sync
.PHONY: runall

collectAndFormatData:
	$(PYTHON) LUcompUncertLab-dataprep.py && $(PYTHON) preprocess.py && echo "data prepared"

interpolate:
	$(PYTHON) interpolate_community_quantiles.py && echo "interpolated over time"

generateForecasts:
	$(PYTHON) buildWeightsForLocations.py && echo "forecasts generated"

postprocess:
	$(PYTHON) postprocess.py && echo "Post process complete"

plotTrajectories:
	$(PYTHON) plotTrajectories.py && echo "Plotted trajectories"

add:
	git add .

commit:
	git commit -m "$(COMMIT)"

push:
	git push

send: add commit push
.PHONY: send

sync:
	rsync -arvz --progress ../LUcompUncertLab-humanjudgement/ ../../../2022FluSightModels/LUcompUncertLab-humanjudgement && \
	make -C ../../../2022FluSightModels/
