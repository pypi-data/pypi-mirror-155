# 2022.6.9  restore
from common import * 

def run():
	tid	= st.experimental_get_query_params().get('tid', ['restore'])[0] 
	uid = st.experimental_get_query_params().get('uid', ['0'])[0]

	st.title(hget(f"config:rid-{rid}:tid-{tid}","title", "恢复原序")) 
	st.caption(hget(f"config:rid-{rid}:tid-{tid}","subtitle")) 

	snts = json.loads(hget(f"config:rid-{rid}:tid-{tid}","snts", "[]")) 
	refers = json.loads( hget(f"config:rid-{rid}:tid-{tid}","refers", "[]" ))
	if not refers : refer = [''] * len(snts) 

	labels = [st.text_input( f"[{i+1}] {snt}", hget(f"rid-{rid}:tid-{tid}:uid-{uid}",f"label-{i}") ) for i, snt in enumerate(snts)]
	if st.button("submit") : 
		score = round(100 * len([snt for snt, refer in zip(labels, refers) if snt == refer]) / len(snts), 2)
		st.metric("SCORE", score )
		redis.r.hset(f"rid-{rid}:tid-{tid}:uid-{uid}","score", score, {"rid": rid, "tid": tid,"uid": uid, "type":"restore" } )
		redis.r.hset(f"score:rid-{rid}:tid-{tid}", uid, score) # verbose, for counting convenience
		for i, label in enumerate(labels): 
			#redis.r.hset(f"rid-{rid}:tid-{tid}:uid-{uid}",f"label-{i}", label, {f"score-{i}": 1 if label == refers[i] else 0} )
			redis.r.hset(f"rid-{rid}:tid-{tid}:uid-{uid}",f"label-{i+1}", label, {f"score-{i+1}": 1 if label == refers[i] else 0} )

if __name__ == '__main__': run()