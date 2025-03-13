FROM mcr.microsoft.com/devcontainers/anaconda:1-3

# Copy environment.yml (if found) to a temp location so we update the environment. Also
# copy "noop.txt" so the COPY instruction does not fail if no environment.yml exists.
COPY environment.yml* .devcontainer/noop.txt /tmp/conda-tmp/

RUN if [ -f "/tmp/conda-tmp/environment.yml" ]; then umask 0002 && /opt/conda/bin/conda env update -n base -f /tmp/conda-tmp/environment.yml; fi \
    && rm -rf /tmp/conda-tmp

# Install dependencies for Ollama and other tools
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends \
    curl \
    ca-certificates \
    docker.io \
    docker-compose

# Install Ollama with CPU-only mode
ENV OLLAMA_HOST=0.0.0.0
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install additional Python packages
RUN pip install requests jupyter python-dotenv pandas numpy matplotlib scikit-learn

# Create a script to start services
COPY .devcontainer/start-services.sh /usr/local/bin/start-services.sh
RUN chmod +x /usr/local/bin/start-services.sh