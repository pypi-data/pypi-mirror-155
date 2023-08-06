# generalpackager
Tools to interface GitHub, PyPI and local modules / repos. Used for generating files to keep projects dry and synced. Tailored for my general packages.

This package and 6 other make up [ManderaGeneral](https://github.com/ManderaGeneral).

## Information
| Package                                                              | Ver                                                 | Latest Release        | Python                                                                                                                   | Platform        |   Lvl | Todo                                                        | Tests   |
|:---------------------------------------------------------------------|:----------------------------------------------------|:----------------------|:-------------------------------------------------------------------------------------------------------------------------|:----------------|------:|:------------------------------------------------------------|:--------|
| [generalpackager](https://github.com/ManderaGeneral/generalpackager) | [0.3.14](https://pypi.org/project/generalpackager/) | 2022-06-21 09:13 CEST | [3.8](https://www.python.org/downloads/release/python-380/), [3.9](https://www.python.org/downloads/release/python-390/) | Windows, Ubuntu |     5 | [9](https://github.com/ManderaGeneral/generalpackager#Todo) | 86.7 %  |

## Contents
<pre>
<a href='#generalpackager'>generalpackager</a>
├─ <a href='#Information'>Information</a>
├─ <a href='#Contents'>Contents</a>
├─ <a href='#Installation'>Installation</a>
├─ <a href='#Attributes'>Attributes</a>
└─ <a href='#Todo'>Todo</a>
</pre>

## Installation
| Command                       | <a href='https://pypi.org/project/generallibrary'>generallibrary</a>   | <a href='https://pypi.org/project/generalfile'>generalfile</a>   | <a href='https://pypi.org/project/generalmainframe'>generalmainframe</a>   | <a href='https://pypi.org/project/pandas'>pandas</a>   | <a href='https://pypi.org/project/gitpython'>gitpython</a>   | <a href='https://pypi.org/project/requests'>requests</a>   | <a href='https://pypi.org/project/pyinstaller'>pyinstaller</a>   |
|:------------------------------|:-----------------------------------------------------------------------|:-----------------------------------------------------------------|:---------------------------------------------------------------------------|:-------------------------------------------------------|:-------------------------------------------------------------|:-----------------------------------------------------------|:-----------------------------------------------------------------|
| `pip install generalpackager` | Yes                                                                    | Yes                                                              | Yes                                                                        | Yes                                                    | Yes                                                          | Yes                                                        | Yes                                                              |

## Attributes
<pre>
<a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/__init__.py#L1'>Module: generalpackager</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Class: GitHub</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: download</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: get_description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: get_owners_packages</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: get_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: get_website</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/shared.py#L1'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: set_description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: set_topics</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/github.py#L1'>Method: set_website</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_module.py#L1'>Class: LocalModule</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_module.py#L1'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_module.py#L1'>Method: get_all_local_modules</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_module.py#L1'>Method: get_dependants</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_module.py#L1'>Method: get_dependencies</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_module.py#L1'>Method: get_env_vars</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/shared.py#L1'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_module.py#L1'>Property: module</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_module.py#L1'>Property: objInfo</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Class: LocalRepo</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: bump_version</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: create_sdist</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: description</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: enabled</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: extras_require</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: format_file</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: generate_exe</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_exeproduct_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_exetarget_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_generate_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_git_exclude_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_init_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_license_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_manifest_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_metadata_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_metadata_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_org_readme_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_package_paths_gen</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_path_from_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_randomtesting_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_readme_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_repo_path_child</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_repo_path_parent</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_repos_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_setup_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_test_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_test_paths</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_test_template_path</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: get_workflow_path</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: git_changed_files</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: has_metadata</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: install_requires</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/shared.py#L1'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: load_metadata</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: manifest</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: path_exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: pip_install</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: pip_uninstall</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: private</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: replace_camel_case</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: replace_docstrings</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: text_in_tests</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: unittest</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: upload</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Property: version</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/local_repo.py#L1'>Method: write_metadata</a>
├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager.py#L1'>Class: Packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_github.py#L1'>Method: commit_and_push</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: compare_local_to_github</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: compare_local_to_pypi</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: create_blank_locally</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager.py#L1'>Method: exists</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: filter_relative_filenames</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_relations.py#L1'>Method: general_bumped_set</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_relations.py#L1'>Method: general_changed_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_generate</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_git_exclude</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_init</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_license</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_localfiles</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_manifest</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_personal_readme</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_randomtesting</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_readme</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_setup</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_test_template</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: generate_workflow</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: get_attributes_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: get_badges_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_metadata.py#L1'>Method: get_classifiers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_relations.py#L1'>Method: get_dependants</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_relations.py#L1'>Method: get_dependencies</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: get_description_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: get_env</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: get_footnote_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: get_information_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: get_installation_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_pypi.py#L1'>Method: get_latest_release</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: get_new_packager</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_relations.py#L1'>Method: get_ordered_packagers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_relations.py#L1'>Method: get_owners_package_names</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: get_sync_job</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: get_todos</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: get_todos_markdown</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_metadata.py#L1'>Method: get_topics</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: get_triggers</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: get_unittest_job</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_relations.py#L1'>Method: get_untested_objInfo_dict</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: github_link</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_markdown.py#L1'>Method: github_link_path_line</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: if_publish_bump</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: if_publish_publish</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_metadata.py#L1'>Method: is_bumped</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/shared.py#L1'>Method: is_general</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_files.py#L1'>Method: relative_path_is_aesthetic</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_pypi.py#L1'>Method: reserve_name</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: run_ordered_methods</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager.py#L1'>Property: simple_name</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager.py#L1'>Method: spawn_children</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager.py#L1'>Method: spawn_parents</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: step_install_necessities</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: step_install_package_git</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: step_install_package_pip</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: step_run_packager_method</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: step_setup_python</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: step_setup_ssh</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: steps_setup</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_github.py#L1'>Method: sync_github_metadata</a>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: upload_package_summary</a> <b>(Untested)</b>
│  ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: workflow_sync</a>
│  └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/packager_workflow.py#L1'>Method: workflow_unittest</a>
└─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/pypi.py#L1'>Class: PyPI</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/pypi.py#L1'>Method: download</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/pypi.py#L1'>Method: exists</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/pypi.py#L1'>Method: get_date</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/pypi.py#L1'>Method: get_owners_packages</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/pypi.py#L1'>Method: get_tarball_url</a>
   ├─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/pypi.py#L1'>Method: get_version</a>
   └─ <a href='https://github.com/ManderaGeneral/generalpackager/blob/f370c53/generalpackager/api/shared.py#L1'>Method: is_general</a>
</pre>

## Todo
| Module                                                                                                                                   | Message                                                                                                                                                                                                  |
|:-----------------------------------------------------------------------------------------------------------------------------------------|:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/local_repo.py#L1'>local_repo.py</a>           | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/local_repo.py#L23'>Search for imports to list dependencies.</a>                                               |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/local_repo.py#L1'>local_repo.py</a>           | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/local_repo.py#L144'>Decoupled JSON serialize instructions with custom dumps in lib.</a>                       |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/local_repo.py#L1'>local_repo.py</a>           | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/local_repo.py#L215'>Make sure twine is installed when trying to upload to pypi.</a>                           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L11'>Move download to it's own package.</a>                                                           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L1'>pypi.py</a>                       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/pypi.py#L65'>Find a faster fetch for latest PyPI version and datetime.</a>                                    |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/github.py#L1'>github.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/api/github.py#L15'>Get and Set GitHub repo private.</a>                                                           |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_markdown.py#L1'>packager_markdown.py</a> | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_markdown.py#L70'>Sort todos by name to decrease automatic commit changes.</a>                            |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L1'>packager.py</a>                   | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager.py#L4'>Prevent workflow using pypi to install a general package.</a>                                     |
| <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L1'>packager_files.py</a>       | <a href='https://github.com/ManderaGeneral/generalpackager/blob/master/generalpackager/packager_files.py#L36'>Watermark generated files to prevent mistake of thinking you can modify them directly.</a> |

<sup>
Generated 2022-06-21 09:13 CEST for commit <a href='https://github.com/ManderaGeneral/generalpackager/commit/f370c53'>f370c53</a>.
</sup>
