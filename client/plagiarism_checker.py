import gensim_similarity as gs

def checkPlagiarism(blockchain, new_transaction):
	alltrans = []
	for block in blockchain:
		for trans in block.transactions:
			alltrans.append((trans, block.index))
	if not alltrans:
		return new_transaction
	alldocs = [x[0]["content"] for x in alltrans]
	pg_index = gs.getPlagiarism(alldocs, new_transaction["content"])
	if pg_index>=0:
		new_transaction["parent_post"] = alltrans[pg_index][0]["post_id"]
		new_transaction["parent_block_index"] = alltrans[pg_index][1]
	return new_transaction