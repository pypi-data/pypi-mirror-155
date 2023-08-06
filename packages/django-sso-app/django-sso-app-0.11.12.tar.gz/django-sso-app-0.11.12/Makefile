DOCKER=docker
DPATH=${CURDIR}
IMAGE_NAME=django-sso-app
#VERSION=$(shell python setup.py --version | sed 's/\.post.*//' | sed 's/\+g.*//')
VERSION=$(shell cd src && python3 -c 'import django_sso_app;print(django_sso_app.__version__)' && cd ..)

export DPATH
.PHONY:	clean build publish build-docker push-docker

clean:
	rm -rf ./dist/*
	rm -rf ./build/*
	rm -rf  ./src/django_sso_app.egg-info
	find ./src -name *.pyc -exec rm {} \;

build-release: clean
	python setup.py sdist bdist_wheel

publish:
	twine upload dist/* --verbose

build-docker: clean
	$(DOCKER) build . --network host -f ./compose/production/django/Dockerfile -t paiuolo/${IMAGE_NAME} -t paiuolo/${IMAGE_NAME}:${VERSION}

push-docker:
	$(DOCKER) push paiuolo/${IMAGE_NAME}:${VERSION}
	$(DOCKER) push paiuolo/${IMAGE_NAME}:latest
