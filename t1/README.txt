Instructions to execute:

The list of dependencies can be found at: dependencias.txt

1. kNN classifier
	Basic, with automatic testing/training division:
		python3 classify.py -i your_csv_file -l training_ratio -o output_file -c column_number_of_class
	where the training_ratio specifies the percentage of the input set that will be used as the training set (e.g 50)
		Example:
		python3 classify.py -i datasets/generoIris2D.csv -l 50 -o output.csv -c 2

	Explicit training set:
		python3 classify.py -i your_csv_file -t training_set_csv_file -o output_file -c column_number_of_class

	Spiral, saving the result as an image:
		python3 classify.py --spiral spiral_type -g grid_size -S -o output_file
	where spiral_type is either 'single' or 'double'.

	Spiral, plotting the result:
		python3 classify.py --spiral spiral_type -g grid_size -p
	where spiral_type is either 'single' or 'double'.

	Using Hamming+ distance instead of euclidean:
		python3 classify.py [any of the above flags] -d hamming+

	Explicit value of k (k-Nearest Neighbor):
		python3 classify.py [any of the above flags] -k value_of_k


	For the full list of options, execute:
		python3 classify.py

2. Voronoi diagram
	Diagram of a 2D CSV dataset:
		python3 voronoi.py -i your_csv_file -c column_number_of_class

	Diagram of a single spiral:
		python3 voronoi.py --singlespiral grid_size [--noise noise_value]

	Diagram of a double spiral:
		python3 voronoi.py --doublespiral grid_size [--noise noise_value]	

3. Mahalanobis distance
	Linear mahalanobis:
		python3 mahalanobis.py -i input_file -o output_file

	Quadratic mahalanobis:
		python3 mahalanobis.py -q -i input_file -o output_file

	L2norm (euclidean distance):
		python3 l2norm.py -i input_file -o output_file

	Comparison between L2norm and/or mahalanobis distance:
		python3 mahalanobis.py -i input_file -o output_file -c alg1 alg2
		OR
		python3 l2norm.py -i input_file -o output_file -c alg1 alg2
	where "alg1" and "alg2" are the algorithms to be compared. It's possible to specify a third algorithm as well. Possible algorithms are:
		l2norm
		linear_mahalanobis
		quadratic_mahalanobis
	each result will be saved to the target output file with the algorithm name appended to it. For example, consider the following command:
		python3 mahalanobis.py -i datasets/flowers.jpg -o output -c l2norm linear_mahalanobis quadratic_mahalanobis
	after finishing execution, the program will display and save three image files:
		output_l2norm
		output_linear_mahalanobis
		output_quadratic_mahalanobis

	After executing any of the commands above, the input iamge will be presented to the user. The user then chooses the desired pixels by dragging the mouse cursor over the image and then closes it. The resulting image(s) will then be displayed and saved.

---------------------------------------------
Instruções para executar:

A lista de dependências encontra-se em: dependencias.txt

1. Classificador kNN
	Básico, com divisão automática entre treinamento e teste:
		python3 classify.py -i seu_arquivo_csv -l proporção_de_treinamento -o arquivo_de_saída -c número_da_coluna_da_classe
	onde proporção_de_treinamento especifica a porcentagem do conjunto de entrada que será usado como conjunto de treinamento (ex: 50)
		Exemplo:
		python3 classify.py -i datasets/generoIris2D.csv -l 50 -o output.csv -c 2

	Conjunto de treinamento explícito:
		python3 classify.py -i seu_arquivo_csv -t arquivo_csv_do_conjunto_de_treinamento -o arquivo_de_saída -c número_da_coluna_da_classe

	Espiral, salvando o resultado como imagem:
		python3 classify.py --spiral tipo_de_espiral -g tamanho_do_grid -S -o arquivo_de_saída
	onde tipo_de_espiral pode ser 'single' ou 'double'.

	Espiral, plotando o resultado:
		python3 classify.py --spiral tipo_de_espiral -g tamanho_do_grid -p
	onde tipo_de_espiral pode ser 'single' ou 'double'.

	Usando distância de Hamming+ ao invés de euclideana:
		python3 classify.py [quaisquer flags acima] -d hamming+

	Valor explícito de k (k-Nearest Neighbor):
		python3 classify.py [quaisquer flags acima] -k valor_de_k

	Para a lista completa de opções, execute:
		python3 classify.py

2. Diagrama de Voronoi
	Para mostrar o diagrama 2D CSV dataset:
		python3 voronoi.py -i seu_arquivo_csv -c número_da_coluna_da_classe

	Diagrama de uma espiral simples:
		python3 voronoi.py --singlespiral tamanho_do_grid [--noise intensidade_de_noise]

	Diagrama de uma espiral dupla:
		python3 voronoi.py --doublespiral tamanho_do_grid [--noise intensidade_de_noise]

3. Distância de Mahalanobis
	Mahalanobis linear:
		python3 mahalanobis.py -i arquivo_de_entrada -o arquivo_de_saida

	Mahalanobis quadrático:
		python3 mahalanobis.py -q -i arquivo_de_entrada -o arquivo_de_saida

	L2norm (distância euclidiana):
		python3 l2norm.py -i arquivo_de_entrada -o arquivo_de_saida

	Comparação entre L2norm e/ou distância de mahalanobis:
		python3 mahalanobis.py -i arquivo_de_entrada -o arquivo_de_saida -c alg1 alg2
		OU
		python3 l2norm.py -i arquivo_de_entrada -o arquivo_de_saida -c alg1 alg2
	onde "alg1" e "alg2" são os algoritmos a serem comparados. Também é possível especificar um terceiro algoritmo. Os possíveis algoritmos são:
		l2norm
		linear_mahalanobis
		quadratic_mahalanobis
	cada resultado será salvo ao arquivo de saída alvo com o nome de cada algoritmo concatenado a ele. Por exemplo, considere o seguinte comando:
		python3 mahalanobis.py -i datasets/flowers.jpg -o output -c l2norm linear_mahalanobis quadratic_mahalanobis
	após o término da execução, o programa exibirá e salvará três arquivos de imagem:
		output_l2norm
		output_linear_mahalanobis
		output_quadratic_mahalanobis

	Após executar qualquer um dos comandos acima, a imagem de entrada será apresentada ao usuário. O usuário então escolhe os pixels desejados arrastando o clique do mouse sobre a imagem e então a fecha. A(s) imagem(ns) resultante(s) será(ão) então exibida(s) e salva(s).
