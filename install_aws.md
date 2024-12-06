## Guia de Instalação da CoreHiveAI no AWS (54.159.232.157)

### 1. Conectar à Instância
```bash
ssh -i sua-chave.pem ubuntu@54.159.232.157
```

### 2. Configurar Firewall
```bash
sudo ufw allow 22/tcp
sudo ufw allow 5000/tcp
sudo ufw allow 5001/tcp
sudo ufw enable
```

### 3. Instalar Dependências
```bash
# Atualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Python e ferramentas
sudo apt install python3-pip python3-venv git nginx certbot python3-certbot-nginx -y

# Clonar repositório
git clone https://seu-repositorio/corehiveai.git
cd corehiveai

# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 4. Configurar SSL com Certbot
```bash
sudo certbot --nginx -d seu-dominio.com
```

### 5. Configurar Variáveis de Ambiente
```bash
sudo nano /etc/environment

# Adicionar as linhas:
COREHIVEAI_API_KEY="sua-chave-api-secreta"
COREHIVEAI_ENV="production"
```

### 6. Configurar Serviços
```bash
# Nó principal
sudo nano /etc/systemd/system/corehiveai-node.service

[Unit]
Description=CoreHiveAI Node
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/corehiveai
Environment="PATH=/home/ubuntu/corehiveai/venv/bin"
Environment="COREHIVEAI_ENV=production"
Environment="COREHIVEAI_API_KEY=sua-chave-api-secreta"
ExecStart=/home/ubuntu/corehiveai/venv/bin/python blockchain/node.py
Restart=always

[Install]
WantedBy=multi-user.target

# API de desenvolvedores
sudo nano /etc/systemd/system/corehiveai-dev.service

[Unit]
Description=CoreHiveAI Developer API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/corehiveai
Environment="PATH=/home/ubuntu/corehiveai/venv/bin"
Environment="COREHIVEAI_ENV=production"
Environment="COREHIVEAI_API_KEY=sua-chave-api-secreta"
ExecStart=/home/ubuntu/corehiveai/venv/bin/python apps/developer_api.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 7. Iniciar Serviços
```bash
sudo systemctl daemon-reload
sudo systemctl enable corehiveai-node
sudo systemctl enable corehiveai-dev
sudo systemctl start corehiveai-node
sudo systemctl start corehiveai-dev
```

### 8. Configurar Backup Automático
```bash
# Instalar AWS CLI
sudo apt install awscli -y

# Configurar credenciais AWS
aws configure

# Criar script de backup
sudo nano /usr/local/bin/backup-blockchain.sh

#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/home/ubuntu/backups"
DB_FILE="/home/ubuntu/corehiveai/blockchain.db"

mkdir -p $BACKUP_DIR
sqlite3 $DB_FILE ".backup '$BACKUP_DIR/blockchain_$DATE.db'"
aws s3 cp $BACKUP_DIR/blockchain_$DATE.db s3://seu-bucket/backups/

# Tornar executável
sudo chmod +x /usr/local/bin/backup-blockchain.sh

# Adicionar ao crontab
(crontab -l 2>/dev/null; echo "0 */6 * * * /usr/local/bin/backup-blockchain.sh") | crontab -
```

### 9. Monitoramento
```bash
# Instalar Prometheus Node Exporter
sudo apt install prometheus-node-exporter -y

# Configurar CloudWatch
sudo apt install amazon-cloudwatch-agent -y
sudo /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-config-wizard
```

### 10. Logs e Monitoramento
```bash
# Verificar logs
sudo journalctl -u corehiveai-node -f
sudo journalctl -u corehiveai-dev -f

# Monitorar recursos
htop
```

### Notas de Segurança:
1. Mantenha o sistema atualizado regularmente
2. Faça backup do banco de dados a cada 6 horas
3. Monitore os logs em busca de atividades suspeitas
4. Use senhas fortes e chaves API seguras
5. Mantenha backups em múltiplas regiões AWS

### Escalabilidade:
- Configure Auto Scaling Group para alta disponibilidade
- Use Amazon RDS para o banco de dados em produção
- Implemente Amazon ElastiCache para melhor performance
- Configure AWS WAF para proteção contra ataques