---
title: LLM을 이용한 자동 스크립트 생성 해보기
author: KimKitae
date: 2024-08-02 12:00:00 +9000
categories: [Automation, Testing, AI]
tags: [Testing, AI]
pin: true
---

최근 ChatGPT의 발전으로 IT 업계에는 많은 변화가 이루어졌습니다. 특히, QA 업계에서는 많은 사람들이 AI가 우리의 자리를 대체할지 걱정했지만, LLM(대규모 언어 모델)은 아직까지는 단어 예측 모델로, 학습한 것 외에는 창의적인 것에는 한계가 존재합니다. AI는 아직까지는 우리를 대체하지 못할 것이지만, AI를 올바르게 사용하지 못하는 사람들은 금방 대체될 가능성이 큽니다.

이번 글에서는 LLM을 이용한 자동화 스크립트 자동 생성 구현 과정을 정리해보려고 합니다. 

다음과 같은 단계를 거쳐 구현하였습니다:
1. LLM 준비
2. 데이터 임베딩
3. 데이터 검색
4. LLM에게 질문과 검색결과 전달
5. LLM 답변


## LLM 모델 선택하기
LLM에는 `ChatGPT`, `Llama3`, `Claude` 등 다양한 모델들이 존재합니다. 본인의 환경에 맞게 선택하면 됩니다. 저는 데이터 유출을 피하고자, 로컬 환경에서 구동할 수 있는 Llama3 모델을 선택하였습니다. MacBook의 경우 GPU가 없기 때문에 LLM 구동에 한계가 있으므로 Ollama를 활용하여 하드웨어 가속을 사용하였습니다. 이를 통해 CPU만으로도 최대한 성능을 얻을 수 있도록 하였습니다.

## 데이터 학습
우리가 원하는 답을 얻기 위해서는 그에 맞는 데이터를 학습시킬 필요가 있습니다. 다만, `Fine-tuning` 에는 많은 비용이 발생합니다. 여러 데이터 학습 기법 중 `Mlx-lm` 을 이용하여 `Lora` 로 학습을 시켜보니 사용되는 메모리는 `130GB` 였습니다. 스크립트 내 함수들은 자주 변경되므로 그때마다 학습시키는 것은 적합하지 않았습니다. 따라서 RAG(Retrieval-Augmented Generation) 방법으로 필요한 데이터를 검색하여 LLM이 참조할 수 있도록 하여 항상 최신 데이터 기반으로 답변을 받도록 하였습니다.


### RAG란?
RAG는 Retrieval-Augmented Generation의 약자로, LLM의 성능을 향상시키기 위해 외부 데이터를 검색하여 활용하는 방법입니다. 이 방법은 LLM이 모든 정보를 기억해야 하는 부담을 덜어주고, 실시간으로 정보를 검색하여 최신 데이터를 활용할 수 있도록 합니다. RAG는 크게 세 단계로 이루어져 있습니다: 임베딩, 검색, 그리고 컨텍스트 생성입니다.



## 임베딩
임베딩은 텍스트 데이터를 벡터로 변환하는 과정입니다. 이 과정은 LLM이 텍스트를 이해하고, 비슷한 의미의 문장들을 유사한 벡터로 표현할 수 있도록 합니다. 임베딩된 벡터는 고차원의 공간에서 의미론적으로 비슷한 텍스트끼리 가까이 위치하게 되어, 나중에 유사한 내용을 쉽게 찾을 수 있게 합니다.

`Ollama` 를 통해 `mxbai-embed-large` 모델을 이용하여 벡터화 합니다.

```
def get_embedding(text, model_name="mxbai-embed-large"):
    """
    입력 텍스트를 임베딩 벡터로 변환합니다.
    """
    url = f"{OLLAMA_API_BASE}/embeddings"
    data = {
        "model": model_name,
        "prompt": text
    }
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        embedding = response.json().get('embedding')
        if not embedding:
            logger.error(f"임베딩 반환 실패: {text[:50]}...")
            return None
        return np.array(embedding, dtype=np.float32)
    except requests.RequestException as e:
        logger.error(f"임베딩 획득 오류: {e}")
        return None
```


## 검색
임베딩 과정을 통해 생성된 벡터를 기반으로, LLM은 질문에 적합한 정보를 외부 데이터베이스나 문서에서 검색할 수 있습니다. 검색 단계에서는 사용자가 입력한 질문과 가장 관련성이 높은 정보를 찾아내는 것이 중요합니다. 많은 벡터 데이터베이스 중 저는 `Faiss-cpu`를 이용하여 임베딩 데이터를 저장 및 검색합니다.

- Index 파일 생성 및 DB 적재
```
def create_index(scripts, max_chunks_per_script=10, max_chunk_size=100):
    """
    스크립트 목록을 사용하여 FAISS 인덱스를 생성합니다.
    """
    embeddings = []
    chunked_scripts = []

    def process_script(script):
        chunks = chunk_text(script['content'], chunk_size=max_chunk_size, overlap=25)[:max_chunks_per_script]
        script_embeddings = []
        script_chunks = []
        for chunk in chunks:
            embedding = get_embedding(chunk)
            if embedding is not None:
                script_embeddings.append(embedding)
                script_chunks.append({
                    'path': script['path'],
                    'content': chunk
                })
        return script_embeddings, script_chunks

    logger.info(f"스크립트 처리 시작: 총 {len(scripts)}개 스크립트")
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(process_script, script) for script in scripts]
        for future in as_completed(futures):
            script_embeddings, script_chunks = future.result()
            embeddings.extend(script_embeddings)
            chunked_scripts.extend(script_chunks)

    logger.info(f"총 {len(chunked_scripts)}개의 청크 생성됨")
    logger.info(f"총 {len(embeddings)}개의 임베딩 생성됨")

    if not embeddings:
        logger.error("유효한 임베딩 생성 실패")
        return None, None

    # 임베딩 차원 확인 및 로깅
    embedding_dimensions = [len(emb) for emb in embeddings]
    if len(set(embedding_dimensions)) != 1:
        logger.error(f"임베딩 차원이 일치하지 않음: {set(embedding_dimensions)}")
        return None, None

    dimension = embedding_dimensions[0]
    logger.info(f"임베딩 차원: {dimension}")

    # numpy 배열로 변환
    embeddings_array = np.array(embeddings, dtype=np.float32)
    logger.info(f"임베딩 배열 shape: {embeddings_array.shape}")

    # FAISS 인덱스 생성
    index = faiss.IndexHNSWFlat(dimension, 32)
    index.add(embeddings_array)
    logger.info(f"{len(embeddings)}개의 임베딩으로 인덱스 생성 완료")

    # 인덱스 기본 정보 로깅
    logger.info(f"FAISS 인덱스 정보:")
    logger.info(f"  - 총 벡터 수: {index.ntotal}")
    logger.info(f"  - 차원: {index.d}")

    return index, chunked_scripts
```

- 질문에 대한 DB 검색, 유사도를 통해 가장 근접한 검색결과 도출하기

```
def search_scripts(query, index, scripts, k=10):
    query_vector = get_embedding(query)
    if query_vector is None:
        logger.error("쿼리에 대한 임베딩 획득 실패")
        return []

    logger.debug(f"쿼리 벡터 차원: {query_vector.shape}")
    logger.debug(f"인덱스 차원: {index.d}")

    try:
        distances, indices = index.search(np.array([query_vector]), k)
        logger.debug(f"검색 결과 - 거리: {distances}, 인덱스: {indices}")

        results = [(scripts[i], float(1 / (1 + distances[0][j]))) for j, i in enumerate(indices[0]) if i < len(scripts)]

        logger.info(f"필터링 전 검색 결과 수: {len(results)}")

        # 임계값 제거
        filtered_results = results

        logger.info(f"필터링 후 검색 결과 수: {len(filtered_results)}")
        return sorted(filtered_results, key=lambda x: x[1], reverse=True)
    except Exception as e:
        logger.error(f"검색 중 오류 발생: {e}")
        return []

def truncate_context(context, max_length=9000):
    """
    너무 긴 문맥을 지정된 최대 길이로 줄입니다.
    """
    if len(context) <= max_length:
        return context
    return context[:max_length] + "..."
```

토큰의 크기가 커질수록, 리소스 사용량은 커집니다. 따라서 적절한 토큰 길이를 지정해주는 것이 좋습니다. 또한 검색 결과 수와 임계값을 조정하여 질문에 가장 근사한 검색 결과를 도출하도록 합니다.

청크 사이즈와 오버랩 크기 설정, 즉 데이터를 어느 크기마다 자를 것인지, 각 자른 데이터의 겹치는 부분을 얼마나 할 것인지에 따라, 다음 문맥의 유사도에 따른 검색 결과는 확연히 달라지므로 이는 직접 수정해보며 가장 알맞은 크기를 찾아야 합니다.


## 컨텍스트 생성
검색된 정보를 바탕으로, LLM은 입력된 질문에 대한 답변을 생성하기 위해 필요한 컨텍스트를 형성합니다. 이 단계에서는 검색된 정보가 질문과 어떻게 연관되는지를 파악하고, 답변에 필요한 핵심 내용을 추출하여 LLM이 활용할 수 있는 형태로 정리합니다.

- 검색결과를 추출하여 Context에 저장하고, System Prompt 를 통해 원하는 답변을 적어, LLM에게 전달 합니다.

```
def ask_ollama(query, context, model_name="automation", max_retries=1):
    """
    OLLAMA API를 사용하여 질문에 대한 응답을 생성합니다.
    """
    url = f"{OLLAMA_API_BASE}/generate"
    
    system_prompt = """
    주어진 컨텍스트와 질문을 주의 깊게 분석하여, 질문에 가장 관련성 높은 example의 스크립트를 제공해주세요.
    컨텍스트에 없는 정보는 절대 사용하지 마세요.
    반드시 컨텍스트 내의 name과 description을 비교하여 질문과 가장 관련성 높은 example의 스크립트를 제공해주세요.
    함수 내 매개변수의 값은 질문의 값으로 변경 가능합니다. 
    질문과 직접적으로 관련이 없는 정보는 제외하고 응답해주세요.
    """

    truncated_context = truncate_context(context, max_length=3000)
    
    prompt = f"""
    컨텍스트:
    {truncated_context}

    질문: {query}
    """

    data = {
        "model": model_name,
        "prompt": prompt,
        "system": system_prompt,
        "stream": False,
        "temperature": 0.0,
        "top_p": 0.5,
        "max_tokens": 500
    }
```

- **temperature** : 숫자가 높을수록 창의적으로 답하게 됩니다. 저는 순수히 검색된 결과에 의한 답변을 원하기 때문에 0.0을 주어 최소한의 다양성을 가지게 하였습니다.
- **top_p** : 수치에 따라 LLM은 다음에 나올 단어를 예측합니다. 값을 높이면 다양한 응답을 하게 되고, 값이 낮을수록 집중적이고 예측 가능한 응답을 얻게 됩니다.
- **max_tokens** : 최대 답변 길이로, 길수록 많은 토큰을 처리해야 하므로 성능적 이슈가 있을 수 있습니다.


## 답변 생성
마지막으로, LLM은 생성된 컨텍스트를 활용하여 사용자의 질문에 적절한 답변을 생성합니다. 이 과정에서 LLM은 검색된 정보를 기반으로 보다 정확하고 최신의 답변을 제공할 수 있게 됩니다. RAG 방법을 통해, LLM은 단순한 예측 모델을 넘어 실제로 유용한 정보를 제공할 수 있는 강력한 도구로 발전할 수 있습니다.

```
    if index is None:
        logger.error("인덱스 생성 실패. 종료합니다.")
        exit(1)

    while True:
        query = input("질문을 입력하세요 ('quit' 입력 시 종료): ")
        if query.lower() == 'quit':
            break

        logger.info(f"사용자 질문: {query}")
        results = search_scripts(query, index, chunked_scripts)

        print("\n관련성 높은 스크립트:")
        if results:
            for result, score in results[:3]:
                print(f"경로: {result['path']}")
                print(f"미리보기: {result['content'][:100]}...")
                print(f"관련도 점수: {score:.4f}")
                print()

            context = " ".join([result[0]['content'] for result in results[:3]])
            answer, full_response = ask_ollama(query, context)
            if answer:
                print("\n관련 스크립트를 바탕으로 한 답변:")
                print(answer)
            else:
                print("답변 생성에 실패했습니다. 로그를 확인해 주세요.")
        else:
            print("관련 스크립트를 찾지 못했습니다. 검색 로직을 확인해 주세요.")
        print()
```

## 결과보기
별도의 `WebUI`가 아닌 TA팀에서 운영하는 SlackBot을 통해 질문을 받고 답변하도록 하여, 구성원 누구나 쉽게 접근할 수 있도록 하였습니다. 예를 들어, `iOS #### 지역 이동 후 #### 매장의 테스트2 메뉴 선택하고, 신용카드로 1000원 포인트 사용하여 결제하는 스크립트 작성해줘` 라는 질문을 던져봅니다.

![Slackbot 답변](https://github.com/user-attachments/assets/0a0c1126-6c5f-46ab-b9b7-f9ecdeec5784)

벡터 DB 내 질문과 유사한 결과들을 참조하여 질문에 맞는 답변을 생성하게 됩니다.
Slackbot을 통해 자동화 스크립트 생성뿐만 아니라 스크립트에 대한 질문 응답을 하도록 하였습니다. Slackbot에서는 답변과 함께, LLM이 참고한 검색 결과도 같이 노출되도록 하였습니다.

## 중요포인트
LLM 선택 은 가장 성능이 좋은 모델을 선택하면 됩니다. 다만, 제일 중요한 점은 `데이터`입니다. 사람이 이해하기 어려운 문서는 LLM도 이해하기 어렵습니다. 최대한 단순화하고, 검색 결과에 잘 도출될 수 있도록 정리를 해야 합니다. 물론 용량이 큰 컨텍스트를 사용하면 정리 중요도는 적을 수 있지만, 컨텍스트는 비용입니다. 최소화된 컨텍스트를 이용하여 적절한 답변을 얻을 수 있도록 데이터 정리를 필수를 하는것이 가장 중요합니다.

이 밖에도, 이와 반대로 Context 비용을 줄이기 위해 자동화 테스트 케이스들의 대한 정보들을 각 `키워드` 에 맞게 미리 생성하고 질문에 대한 `키워드` 추출을 LLM이 하도록 하여 해당되는 `키워드`의 데이터를 반환하도록 하여 token 비용을 최소화하는 방식으로도 운영하여 자동화 테스트 케이스 에 대한 질의응답을 하는 서비스도 운영중에 있습니다. 이 또한 향후 내용 정리해 공유해보록 하겠습니다.