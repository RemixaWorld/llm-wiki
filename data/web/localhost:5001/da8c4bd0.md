---
domain: localhost:5001
fetch_date: '2026-05-18T12:43:13.350377'
note_fallback: true
status: ok
url: http://localhost:5001/v1alpha/convert/source
---

# 本地运行文档解析工具Docling为API服务

Docling 提供了一种用户友好的界面，可以将其作为 API 服务器进行使用。它拥有强大的 API 和详细的文档，适合开发自定义应用程序。此外，Docling 的集成 API 服务器已准备好在不同环境中部署，支持本地基础设施、云平台和 Kubernetes。
- **本地实现通过容器镜像**
  - 通过 Podman 或 Docker 测试 API 服务器的最简单方式是运行以下命令，将其本地端口映射到容器内的端口 5001：
    ```bash
    podman run -p 5001:5001 quay.io/docling-project/docling-serve
    ```
    或者
    ```bash
    docker run -p 5001:5001 quay.io/docling-project/docling-serve
    ```
  - 启动后，您可以通过以下 URL 访问本地服务器：
    - 服务器地址：http://0.0.0.0:5001
    - 文档地址：http://0.0.0.0:5001/docs
    - 用户界面地址：http://0.0.0.0:5001/ui
  - 也可以使用 CURL 命令进行测试：
    ```bash
    curl -X 'POST' 'http://localhost:5001/v1alpha/convert/source' -H 'accept: application/json' -H 'Content-Type: application/json' -d '{"http_sources": [{"url": "https://arxiv.org/pdf/2501.17887"}]}'
    ```

- **本地实现通过代码**
  - **环境准备**
    - 创建一个虚拟环境并激活：
      ```bash
      python3.12 -m venv myenv
      source myenv/bin/activate
      ```
    - 安装依赖：
      ```bash
      pip install --upgrade pip
      pip install "docling-serve"
      ```
    - 运行服务：
      ```bash
      docling-serve run
      ```

  - **示例代码概述**
    - 示例代码采用异步编程，发送 URL 进行转换。代码包含数据的异步传输、错误处理以及写入文件的功能。
    - 访问服务器的 API，并将响应写入 JSON 文件中。

- **使用 GUI**
  - 访问用户界面的方法：
    - 通过容器镜像访问：
      ```bash
      podman run -p 5001:5001 -e DOCLING_SERVE_ENABLE_UI=true quay.io/docling-project/docling-serve
      ```
      或者
      ```bash
      docker run -p 5001:5001 -e DOCLING_SERVE_ENABLE_UI=true quay.io/docling-project/docling-serve
      ```
    - 通过代码访问：
      ```bash
      pip install "docling-serve[ui]"
      docling-serve run --enable-ui
      ```

- **在集群（OpenShift/Kubernetes）上部署**
  - 进行集群环境部署的步骤：
    ```bash
    kubectl apply -f docs/deploy-examples/docling-serve-oauth.yaml
    ```
  - 通过 OpenShift 服务器检索端点及认证令牌：
    ```bash
    DOCLING_NAME=docling-serve
    DOCLING_ROUTE="https://$(oc get routes ${DOCLING_NAME} --template={{.spec.host}})"
    OCP_AUTH_TOKEN=$(oc whoami --show-token)
    ```
  - 测试请求的 CURL 命令：
    ```bash
    curl -X 'POST' "${DOCLING_ROUTE}/v1alpha/convert/source/async" -H "Authorization: Bearer ${OCP_AUTH_TOKEN}" -H "accept: application/json" -H "Content-Type: application/json" -d '{"http_sources": [{"url": "https://arxiv.org/pdf/2501.17887"}]}'
    ```

https://blog.gopenai.com/running-docling-as-an-api-server-54820abc09a6  
https://github.com/docling-project/docling-serve
