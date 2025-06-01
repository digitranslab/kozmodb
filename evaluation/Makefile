
# Run the experiments
run-kozmodb-add:
	python run_experiments.py --technique_type kozmodb --method add

run-kozmodb-search:
	python run_experiments.py --technique_type kozmodb --method search --output_folder results/ --top_k 30

run-kozmodb-plus-add:
	python run_experiments.py --technique_type kozmodb --method add --is_graph

run-kozmodb-plus-search:
	python run_experiments.py --technique_type kozmodb --method search --is_graph --output_folder results/ --top_k 30

run-rag:
	python run_experiments.py --technique_type rag --chunk_size 500 --num_chunks 1 --output_folder results/

run-full-context:
	python run_experiments.py --technique_type rag --chunk_size -1 --num_chunks 1 --output_folder results/

run-langmem:
	python run_experiments.py --technique_type langmem --output_folder results/

run-zep-add:
	python run_experiments.py --technique_type zep --method add --output_folder results/

run-zep-search:
	python run_experiments.py --technique_type zep --method search --output_folder results/

run-openai:
	python run_experiments.py --technique_type openai --output_folder results/
