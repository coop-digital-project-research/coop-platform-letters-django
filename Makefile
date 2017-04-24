SASS_DIR = almanac/assets/sass
SASS_FILES = $(shell find almanac/assets -iname '*.scss')

APP_CSS = almanac/static/css/app.css

.PHONY: all
all: css

.PHONY: clean
clean:
	rm -rf $(APP_CSS)

.PHONY: test
test:
	./test.sh

.PHONY: run
run:
	./manage.py runserver 0.0.0.0:8009

.PHONY: css
css: $(APP_CSS)

$(APP_CSS): $(SASS_FILES)
	@mkdir -p almanac/static/css
	sass $(SASS_DIR)/app.scss $(APP_CSS)

.PHONY: watch
watch:
	@mkdir -p almanac/static/css
	sass --watch --poll $(SASS_DIR)/app.scss:$(APP_CSS)
