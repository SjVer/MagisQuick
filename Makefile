SHELL := /bin/bash

start_all_over:
	rm -r venv
	python3 -m venv venv
	source venv/bin/activate
	which pip
	pip install django

fuck_baseform_bug:
	@echo "in file venv/lib/python3.10/site-packages/django/contrib/admin/checks.py"
	@echo "replace"
	@echo "    \`\`\`"
	@echo "    if not _issubclass(obj.form, BaseModelForm) or t:"
	@echo "            return must_inherit_from("
	@echo '                parent="BaseModelForm", option="form", obj=obj, id="admin.E016"'
	@echo "            )"
	@echo "        else:"
	@echo "            return []"
	@echo "    \`\`\`"
	@echo "with"
	@echo "    \`\`\`"
	@echo "    return []"
	@echo "    \`\`\`"

start:
	source venv/bin/activate

stop:
	source venv/bin/deactivate

migrate:
	python manage.py migrate

freeze:
	python -m pip freeze > requirements.txt

serve:
	clear -x
	python manage.py runserver