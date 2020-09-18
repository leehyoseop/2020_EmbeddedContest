### Description of clothes recommendation codes 😀😀😀😀
👉[당근마켓](https://medium.com/daangn/%EB%94%A5%EB%9F%AC%EB%8B%9D-%EA%B0%9C%EC%9D%B8%ED%99%94-%EC%B6%94%EC%B2%9C-1eda682c2e8c)
👉[추천 개념 참고사이트1](https://lsjsj92.tistory.com/564?category=853217)
👉[추천 개념 참고사이트2](https://yeomko.tistory.com/6)
👉[추천 개념 참고사이트3](https://dnddnjs.github.io/recomm/2019/08/15/recommendation_system_basics/)
<br>😥 공부 먼저하기
#### 추천 시스템 개념
 
    (1) 컨텐츠 기반 필터링 : 사용자가 특정 아이템을 선호하는 경우 그 아이템과 비슷한 콘텐츠를 가진 다른 아이템을 추천해주는 방식
          (EX) 사용자 A가 ItemA에 평점 많이 줌 -> 그 Item은 romantic영화+이수진 감독 -> 이수진 감독의 다른 romantic 영화 추천해줌
          -> 장점: 초반에 사용자에 대한 정보 부족일 때 이방법 사용하면 좋음 => 나중가면 사용 x 
          
    (2) 협력 필터링 : 사용자가 아이템에 매긴 평점, 상품 구매 이력 등의 사용자 행동 양식 기반으로 추천해주는 방식
        🎈 평점 데이터 성격
                (1) Explicit Dataset: 선호와 비선호를 명확하게 구분해준 데이터 셋(ex_ 영화가 좋으면 5점, 안좋으면 1점 이런식)
                      -> 이 경우 학습 방법: 알지 못하는 데이터를 제외한 평점 데이터만으로 사용자의 선호도를 학습 한 다음 추측
                      
                (2) Implicit Dataset: 행동의 빈도수만 기록한 데이터 셋(ex_쇼핑몰에서 관심있는 옷 계속 클릭)
                      -> 이 경우 학습 방법: 알지 못하는 데이터를 포함하여 사용자의 선호도를 학습한 다음 추측
                      
        🎈 KNN(최근접 이웃 기반) : 사용자-아이템 행렬에서 사용자가 아직 평가하지 않은 아이템을 예측하는 것이 목표    
            💡 최근접 이웃 기반은 주로 Pearson 상관계수를 통해 유사도를 구한다
                  - Pearson 상관계수: X가 증가하면 Y도 증가(1에 가까울 수록), X가 감소하면 Y도 감소-1에 가까울 수록)
                  
            + 사용자 기반: 비슷한 고객들이 ~한 Item을 소비했다
                => User-Item기반 행렬을 가지고, User1과 User2가 ItemA~C까지의 평점이 비슷
                      -> Pearson 상관계수 구했는데 1에 가까움
                          -> 이 두 사람은 서로 유사한 Item에 높은 선호도 매긴다고 생각
                              -> 유사한 사용자가 좋아한 Item으로 추천해줌
                
            + 아이템 기반: ~한 Item을 소비한 고객들은 다음과 같은 상품도 구매했다
                => Item-User기반 행렬을 가지고, ItemA와 ItemB는 비슷한 평점을 가짐 -> ItemA와 B는 서로 유사하다고 생각
                    -> 그래서 아직 ItemA에 대해 평가 안한 User4는 ItemB에 높은 점수 줌 -> User4에게 ItemA추천
             
             💡 최근접 이웃 기반 기법은 평점 데이터를 가지고 양의 선형 or 음의 선형 관계를 계산 => 📃Explicit Dataset 사용 적합
             💡 일반적으로 아이템 기반이 좀 더 정확도 높음 => 📃 최근접 이웃 기반 사용할거면 아이템 기반으로 작성 하기
                
         🎈 "Latent Factor Model" : 관찰된 데이터와 잠재되어 있는 데이터를 연결시키는 기법
               -> 주어진 평점 데이터로 아직 알지 못하는 사용자와 아이템의 특성을 찾아내는 것
               [우리에게는 사용자의 평점이 나타난 커다란 행렬이 있을때 사용자와 아이템 두 Latent Factor를 알아내고자 함 -> 💡 Matrix Factorization 기법 사용]
               
               * R 행렬 : 행(USER), 열(Item)으로 각 행렬에 값으로는 사용자가 아이템에 남긴 평점
               * Nf : Matrix Factorization 학습 시에 정하는 임의의 차원 수(📃보통 50~200사이로 결정)
               * X 행렬 : 행(Nf), 열(Nu:User) => 사용자 Latent Factor 행렬  
               * Y 행렬 : 행(Nf), 열(Ni:Item) => 아이템 Latent Factor 행렬
               - X, Y행렬은 우리가 학습시키고자 하는 대상 => 이 행렬들의 값은 아주 작은 랜덤한 값들로 초기화(🚥R에 있는 값을 쪼개어 생성하는 것이 아님!)
               * xu 와 yi는 각각 특정 사용자와 특정 아이템의 특징 벡터 (Nf x 1 크기의 열 벡터 (column vector))
               
               이때, X행렬의 전치행렬을 구하면 Nu * Nf크기의 행렬이 된다. 이를 Y행렬과 곱해주어 Nu * Ni크기의 평점 예측 행렬을 구한다
               예측된 하나의 평점 행렬의 각각의 값들은 예측 평점 수식을 가지고 계산된다
                  🚩 예측 평점 수식: r(ui) = x(u)*y(i) [x는 전치행렬]
                     => 특정 사용자의 Latent Vector와 특정 아이템의 Latent Vector를 곱하여 평점을 계산
               * Optimization :  Gradient Descent와 Alternating Least Squares 
                  => 학습시켜야 하는 곳은 X와 Y 행렬 두개와 이둘은 곱셈으로 묵여 있다(x(u)*y(i) [x는 전치행렬])
                  => 이 둘을 동시에 최적화 시키는 문제는 Non-convex problem으로 NP에 속한다
                  ( 💡 Gradient Descent로 이를 최적화 시키는 것은 너무 느리고 많은 반복 필요->단점 )
                  ( 💡📃 Alternatin Least Squares는 X와 Y 둘 중 하나를 고정시키고 다른 하나를 최적화시킴-> 이과정을 반복하여 최적의 X와 Y를 찾아낸다)
    
                 
               
          
          💡 가장 많이 사용
          💡📃 Implicit Dataset 사용 시 -> 💡 Matrix Factorization 기법 사용
        
========================================================

#### 옷 추천 코드 or 구성
👉[옷 추천 논문 정리1](https://github.com/chullhwan-song/Reading-Paper/issues/56)
👉[옷 추천 논문 정리2](https://github.com/mgibbs1259/Final-Project-Group8)
👉[옷 추천 이화여대](http://www.jksctxml.co.kr/xml2/5004/784/02806815/02806815.html)
* 문제는 딥러닝 추천이 정확할지 알고리즘이 정확할지 모르겠음 -> 시간으로 생각하면 알고리즘으로 작성해야될거 같음
============================================================================

#### 옷 추천
1. 사용자 데이터가 없기 때문에 Contents-based filerting

  - 옷의 속성 정보 + 사용자 프로파일 => 제품 추천
  
2. 데이터가 어느정도 쌓이면 Collaborative filtering