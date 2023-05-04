import boto3
import csv
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    # Detectar o nome do bucket e arquivo
    print(event) 
    
    # Nome do bucket que contém o arquivo a ser processado
    # src_bucket = 'rafawainer-aws-glue-tests'
    src_bucket = event['Records'][0]['s3']['bucket']['name']
    print(f"src_bucket = {src_bucket}")

    # Nome do arquivo a ser processado
    # src_file = '/input/arquivo.txt'
    src_file = event['Records'][0]['s3']['object']['key']
    print(f"src_file = {src_file}") 

    # Nome do bucket para salvar o arquivo .csv processado
    dest_bucket = src_bucket
    print(f"dest_bucket = {dest_bucket}")

    # Nome do arquivo .csv que será gerado
    dest_file = 'input-processed/' + 'arquivo.csv'
    print(f"dest_file = {dest_file}")

    # Obter o objeto S3 do arquivo a ser processado
    obj = s3.get_object(Bucket=src_bucket, Key=src_file)

    # Ler o conteúdo do arquivo
    contents = obj['Body'].read().decode('utf-8')
    print(f"contents original: {contents}")
    
    # Separar os campos do arquivo usando vírgulas como delimitador
    campos = contents.split(',')

    # Remover pontos e vírgulas do valor
    valor = campos[1].replace('.', '').replace(' ', '')
    
    # Recriar o conteúdo do arquivo com o valor atualizado
    contents = ','.join([campos[0], valor, campos[2]])

    print(f"Iniciando a conversao de txt para CSV com newline")
    # Converter o conteúdo para um arquivo CSV
    rows = [contents.split(',')]
    csv_contents = io.StringIO('', newline='')
    writer = csv.writer(csv_contents)
    
    print(f"Adicionando cabecalho no arquivo csv")
    # Adicionar linha de cabeçalho
    writer.writerow(['chpras', 'cod_barras', 'valor'])
    print(f"Cabecalho no arquivo csv adicionado com sucesso")
    
    writer.writerows(rows)
    print(f"Finalizada a conversao com sucesso")
    
    print(f"Iniciando a codificacao do conteudo em sequencia de bytes")
    # Codificar o conteúdo como uma sequência de bytes
    csv_contents_binary = csv_contents.getvalue().encode('utf-8')
    print(f"Finalizada a codificacao do conteudo em sequencia de bytes")

    print(f"Iniciando a criacao de um novo objeto no S3 no formato do CSV")
    # Criar um novo objeto S3 para o arquivo CSV
    s3.put_object(Bucket=dest_bucket, Key=dest_file, Body=csv_contents_binary)  
    print(f"Arquivo csv salvo com sucesso na AWS S3")
    
    print(f"Vou deletar o arquivo txt original na AWS S3")
    # Deletar o arquivo .txt original após salvar o arquivo .csv
    s3.delete_object(Bucket=src_bucket, Key=src_file)
    print(f"Arquivo txt original deletado com sucesso na AWS S3")

    # Chama o Glue Job
    job_name = "my-glue-job"
    job_arguments = {
        '--s3_bucket': dest_bucket,
        '--s3_key': dest_folder + dest_file
    }
    glue.start_job_run(
        JobName=job_name,
        Arguments=job_arguments
    )
    
    # Retornar uma mensagem de sucesso
    return {
        'statusCode': 200,
        'body': 'Arquivo processado com sucesso!'
    }
