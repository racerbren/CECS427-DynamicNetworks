graph [
	comment "This is a sample graph"
	directed 0
	id 42
	label "Hello, I am a graph"
	node [
		id 1
		label "1"
		thisIsASampleAttribute 42
	]
	node [
		id 2
		label "2"
		thisIsASampleAttribute 43
	]
	node [
		id 3
		label "3"
		thisIsASampleAttribute 44
	]
	edge [
		source 1
		target 2
		label "Edge from node 1 to node 2"
	]
	edge [
		source 2
		target 3
		label "Edge from node 2 to node 3"
	]
	edge [
		source 3
		target 1
		label "Edge from node 3 to node 1"
	]
]