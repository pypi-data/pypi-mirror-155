---
gitea: none
include_toc: true
---
![Build Status](https://drone.mcos.nc/api/badges/laboro/laboro/status.svg) ![License](https://img.shields.io/static/v1?label=license&color=orange&message=MIT) ![Language](https://img.shields.io/static/v1?label=language&color=informational&message=Python)

# Laboro

**Laboro** is a workflow manager that helps you to build and run workflows with the lesser possible code typing.

## Development status

**Laboro** is in early *alpha* stage and is not ready for production.

## Status of this documentation

This documentation is an incomplete work in progress and changes may occur as new versions of **Laboro** are released.

## Install

**Laboro** is intended to be run within a container. See the `container/README.md` file to build a custom **Laboro** container image.

The present documentation will only consider the **Laboro** configuration and usage using the **Laboro** container.

However, **Laboro** is available through the [*Python Package Index*](https://pypi.org/project/laboro/) for adventurous and expert users willing to simply install **Laboro** on their computer using `pip3 install laboro` and configure it manually.

To get the latest **Laboro** version, run the following command line:

```bash
docker pull mcosystem/laboro:latest
```

The **Laboro** version matches the *Python* **Laboro** package version.
Thus, to install **Laboro** in a specific version, use the corresponding tag:

```bash
docker pull mcosystem/laboro:1.0.0
```


## Configuration

**Laboro** has two configuration levels:

- **The global configuration level:**

  This level is set up with the mandatory `/etc/laboro/laboro.yml`.

  The default global configuration file is auto-generated **at build time** from the parameters given to container build command. See the `container/README.md` for further details on the available configuration parameters and how to build a custom **Laboro** container image.

  Passing parameters at build time ascertains that all needed directories are created with the expected permissions.

  Even if **Laboro** is a container based app, modification of the default global configuration  file outside build time (i.e. by mounting a volume at run time) is not expected nor supported.

  If you choose to do so, please, don't forget to create the directories according to your configuration file and apply the right permissions to them.

  Example of global configuration file:
  ```YAML
  ---
  laboro:
    histdir: /opt/laboro/log/hist
    workspacedir: /opt/laboro/workspaces
    workflowdir:  /opt/laboro/workflows
    log:
      dir:  /opt/laboro/log
      level: DEBUG
  ```

- **The workflow configuration level:**

  Each workflow **must** have a *YAML* configuration file in the `${LABORO_WORKFLOWDIR}`.

  The name of the configuration filename **must reflect the workflow name**.
  Thus, if you workflow name is `my_workflow`, the workflow configuration file **must** be `${LABORO_WORKFLOWDIR}/my_workflow.yml`

  The `${LABORO_WORKFLOWDIR}` is expected to be mounted as a container volume at run time.

  Thus, to run the two `my_workflow_1` and `my_workflow_2`, the volume **must** contain `my_workflow_1.yml` and `my_workflow_2.yml` file and be mounted under the `${LABORO_WORKFLOWDIR}` directory which defaults to `${LABORO_HOMEDIR}/workflows`.

  Using the default global configuration file, the following command line would run the `my_workflow_1` and `my_workflow_2` workflows with their corresponding configuration files situated on the container host in the `/path/to/local/dir` directory:

  ```bash
  docker run --name laboro \
             -e TZ=Pacific/Noumea \
             -v /path/to/local/dir:/opt/laboro/workflows:ro \
             mcosystem/laboro \
             -r my_workflow_1 my_workflow_2
  ```

## Workflows

### Sessions

Each execution of a specific workflow is identified by a unique identifier called a `session`. The `session` identifier is a string representation of an [`uuid.uuid4`](https://docs.python.org/3/library/uuid.html?highlight=uuid#uuid.uuid4) object. This session identifier is stored in the [workflow execution history file](#execution-history).

The [workflow log file](#logging) and the [session `workspace`](#workspaces) are named after this property.

### Specification

The workflow configuration file must validate against the specification found [in the source code](./src/laboro/config/manager/schema/workflow.yml)

### Configuration

A workflow is described by a simple *YAML* file describing all details of the workflow steps and actions.

An example of a valid workflow configuration file can be found in the [test suite](./tests/files/workflow_conf.yml)

#### Workflow properties

`name`: The workflow name. This property is used to identify the workflow. The workflow main [workspace](#workspaces), the [workflow log file](#logging) and the workflow [execution history file](#execution-history) are named after this property.

#### Sections

##### packages

The `packages` section lists all *Python* packages that should be installed to run the workflow.

All *Python* packages declared in the `packages` section will be automatically installed using `pip` and made available to the workflow.

However, to avoid hazardous python package installation, any valid **Laboro** package name **must** match the `^laboro_.*$` regular expression and **must** be available through the [*Python Package Index*](https://pypi.org/)

##### workspace

The `workspace` section provides the ability to manage the automatic [workspace](#workspaces) deletion with the `delete_on_exit` sub-property.

When `delete_on_exit` is set to `True`, the session *workspace* is deleted the workflow execution ends.

##### steps

The `steps` section describes all task that will be sequentially executed in the same order that they are listed. Each *step* has its own set of properties.

##### steps.actions

##### steps.action.object

###### steps.action.object.module

###### steps.action.object.class

###### steps.action.object.args

###### steps.action.object.args

###### steps.action.object.instantiate

###### steps.action.object.methods

##### Conditional execution

##### Loops

#### Optional modules loading

A **Laboro** module is a *Python* package specifically designed to run as a **Laboro** extension and provides various classes derived from the `laboro.module.Module` base class (see [the module section](#modules) for further details on **Laboro** modules).

**Laboro** modules needed by the workflow should be listed in the [`packages` section](#packages) of the workflow configuration file.

### Run your workflows

Once the **Laboro** container is built or installed from the official image, you can run you workflows by summoning the container and pass your workflows names as arguments.

The workflows will be run sequentially in the specified order.

```bash
docker pull mcosystem/laboro:latest
docker run --name laboro \
           -v /path/to/local/dir:/opt/laboro/workflows:ro \
           laboro \
           --run my_workflow_1 my_workflow_2
```

Example of a **Laboro** container running a workflow named `my_workflow_2` :
![Laboro demonsration](./media/demo.svg)


## Workspaces

Each [workflow](#workflows) has a file storage space named after [workflow name](#workflow-properties) the and situated under the `${workflowdir}` directory.

The `workspace` is the sub-directory named after the [workflow session id](#sessions) created under the main workflow directory for each workflow execution. [**Laboro** modules](#modules) can use this *workspace* to store file for later use.

**Note*:* When the [`workspace.delete_on_exit` workflow property](#workspace) is set to `True`, the `workspace` and its content is deleted at the end of the workflow execution.

```
-+-- workspacedir/
       |
       +-- my_workflow_1/
       |      |
       |      +-- workflow_1_session_1/
       |      |        |
       |      |        + file_1
       |      |
       |      +-- workflow_1_session_2/
       |               |
       |               + file_1
       |
       +-- my_workflow_2/
              |
              +-- workflow_2_session_1/
              |        |
              |        + file_1
              |
              +-- workflow_ 2_session_2/

```

## Logging

### Log levels

### Log date and time

## Secrets

## Execution history

## Modules

### Available Modules

### Build your own module

#### Write the module specification
