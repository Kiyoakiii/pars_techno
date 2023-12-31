- tv, laptop, pk, cpu, gpu - в них хранится обработанные данные и два файла data analysis_tv.ipynb, data_processing.ipynb
- data analysis_tv.ipynb - тут анализ и поиск схожих объектов
- data_processing.ipynb - тут обработка данных, полученных с сайта
- citilink - содержит 5 папок tv, laptop, pk, cpu, gpu. В каждой папке парсер ссылок и данных по ссылкам(в формате .ipynb, так как это удобнее), link.csv - ссылки на товары, data.csv - данные с сайта, полученные по ссылкам.

# Матчинг
### 📝💡🎯Постановка задачи
Мониторинг конкурентов: парсинг данных о деятельности конкурентов в социальных сетях для отслеживания цен и реакции аудитории. 
Необходимо было спарсить два сайта, сделать обработку данных, для каждого товара с первого сайта найти наиболее похожий со второго, провести анализ похожих товаров. 
### ➡️🔍💡Метод решения
Для того чтобы спарсить данные я использовал библиотеку ```Python Selenium```, предварительно попытавшись использовать ```Request``` и ```BeautifulSoup```. Обработка данных была выполнена путем анализа данных: нахождения общих характеристик товаров, сравнения их значений, приведение их к общему виду. Нахождение наиболее похожего товара реализовал с помощью расстояния Левенштейна и метода k-ближайших соседей. 
### ✋😮🤔Проблемы и решения

На начальных этапах работы была предпринята попытка получения данных с портала DNS. В силу возникших трудностей, связанных с безопасностью, не позволяющих воспользоваться возможностями инструментария Selenium, после ручной проверки работоспособности сайта  было принято решение собирать данные с портала Eldorado. Сначала для нахождения определенной кнопки или названия на сайта я использовал название класса. Потом я начал использовал путь до объекта, что значительно упростило парсинг. Далее во всей работе я использовал именно его, за редким исключением. 

Реализовав парсинг первой страницы товаров, я приступил к переходу на другую страницу и тут возникла проблема. Каждый раз когда я получал данные о товаре, я не мог просто вернуться назад (так как у сайта стояла защита) и мне приходится заново идти от каталога телевизоров  до следующего товара на первых страницах, но на 17 странице (это примерно 550-ый товар) это стало занимать слишком много времени. Пришла идея: сначала спарсить ссылки всех товаров, пройдясь один раз по всем страницам, а потом по этим ссылкам уже переходить и брать нужные данные. 

Написав первый раз код и запустив его, я получил блокировку, которая не позволяла открыть любые ссылки на сайте. Как выяснилось, проблема возникала из-за слишком быстрого парсинга. Поставив ```time.sleep-ы```, я начал обходить данную блокировку. ```time.sleep-ы``` надо было поставить в область кода, отвечающую за обход этой блокировки, а также в обычный цикл парсинга, то есть при каждом новом переходе по ссылке товара программа останавливалась на 2 секунды (не 1, так как ловил блокировку). Решив эту проблему, я спарсил около 500 страниц телевизоров, это заняло у меня около 2 часов (процесс парсинга). 
Аналогично для ноутбуков, компьютеров, процессоров и видеокарт реализовал код, который парсил данные. Тут были мелкие проблемы с тем, что для разных категорий могут быть разные пути до объектов, добавив в try except новый путь проблемы решались. 

Далее необходимо было выбрать второй магазин (конкурент). Мною был выбран Citilink. По началу тут все было даже проще чем с Eldorado. Скачав ссылки на товары,  написав код парсера и запустив код, и он спарсил 500 товаров. После чего я словил блокировку по ip. Обойти ошибку мне помог VPN. Первый раз, когда я пытался спарсить с подключением VPN, я также получили блокировку. Однако была возможность использовать другие сервера. Дальше этой ошибки не было. Появлялись другие ошибки, но они исправлялись быстро. В итоге мною было затрачено на это довольно много времени, около 55 часов. 

Обработку табличных данных, как и парсинг я делал впервые. На данный процесс был затрачен весь день ~ часов 14 на то, чтобы привести данные из одной таблицы и данные из другой таблицы к общему виду. Просматривал колонки из одной таблицы, искал похожие колонки из другой, после чего переименовывал колонки одним названием. На этом этапе происходил отсев признаков (характеристик). Потом я брал пересечения названий колонок и писал функцию, которая обрабатывает исходные таблицы так, чтобы они были одного формата. Тут же делал категориальные признаки числовыми. Названия  были обработаны так, чтобы они обладали максимальной схожестью. Все это было проделано для каждой категории товаров. 

Похожесть товаров я искал двумя методами. Первый метод заключается в том, чтобы использовать расстояние Левенштейна, а второй в использовании машинного обучения. С расстоянием Левенштейна не возникло особых трудностей. Я брал название товара из одной таблицы, сравнивал его со всеми названиями из таблицы конкурентов и брал минимальное расстояние. После чего сопоставлял названия и проверял часть результатов, просматривая их. Несколько раз приходилось улучшать функцию препроцессинга названия товара. 

Что касается машинного обучения, то я решил использовать метод k-ближайших соседей. Выбрал в качестве метрики расстояния Минковского. p = 2, то есть Евклидово расстояние. Выбрал эту метрику,  так как разница между расстояниями при просмотре выглядела логично. Сначала я считаю это расстояние, потом беру три индекса товара (k=3), которые соответствуют наименьшим расстояниям. Затем использую расстояние Левенштейна для поиска среди этих 3 потенциально похожих товаров. Так я получаю похожий товар, используя машинное обучение. Этот способ работает хуже, чем обычное расстояние Левенштейна. 
Так же для каждого типа товаров я делаю кластеризацию, которую далее нигде не используется , однако это визуально помогает разобраться в данных. 

Последнее - это визуализация того, что получилось. Я вывожу boxlpot, гистограмму, и диаграмму. По три графика для результатов двух алгоритмов. Графики распределения, изображенные на рисунке 1, и процентного соотношения, изображенные на рисунке 2, позволяют понять на сколько у конкурентов больше отзывов, какие это отзывы по сравнению с нашими (лучше/хуже). Также дают понять как сильно цена у конкурентов отличается от нашей (больше/меньше).

![image](https://github.com/Kiyoakiii/pars_techno/assets/113302248/176f254c-7cad-4a59-a910-9f71eeabeaf0)

Рисунок 1 - Распределение цены, рейтинга, количества отзывов для CPU


![image](https://github.com/Kiyoakiii/pars_techno/assets/113302248/6180866a-13ca-4658-ac87-c5270b816fd0)
Рисунок - 2 Гистограммы цены, рейтинга, количества отзывов для CPU


На рисунках 2 жирной линией внутри прямоугольника показано медианное значение товаров. Исходя из этих рисунков можно сделать вывод, что у магазина Citilink более высокая оценка по таким критериям, как количество отзывов, средний рейтинг и стоимость товара. Здесь идет статистика по схожим товарам, следовательно, для потребителя магазин Citilink более выгодный и надежный. 

### 🔎📋🔗Алгоритм парсинга

1. Устанавливаются опции для веб-драйвера Chrome и создается экземпляр драйвера:
    - Устанавливаются опции Chrome для блокировки уведомлений;
    - Задается стратегия загрузки страницы ```normal```;
    - Создается экземпляр драйвера Chrome с использованием опций;
2. Максимизируется окно браузера;
3. Открывается веб-страница "https://www.eldorado.ru/d/kompyuternye-komplektuyushchie/";
4. Производится прокрутка страницы вниз;
5. Удаляется элемент, который перекрывает интересующую информацию на странице;
6. Выполняется нажатие на элемент для перехода на следующую страницу;
7. Проверяется наличие ошибки "Access to resource was blocked." на странице. Если ошибка обнаружена, производится переход на страницу "https://www.eldorado.ru/d/kompyuternye-komplektuyushchie/" и удаляется перекрывающий элемент (если есть);
8. Загружается CSV-файл с ссылками на товары;
9. Задаются начальные значения переменных: ```start_page = 1, start_card = 1, number_of_reviews = (start_page - 1) * 34```;
10. Начинается цикл по страницам (от ```start_page``` до ```10```);
11. Внутри цикла происходит парсинг ссылок на товары:
ищется элемент, содержащий ссылку на товар, и сохраняется его адрес в словарь ```link```;
    - Ссылка добавляется в DataFrame ```data_link```;
    - DataFrame ```data_link``` сохраняется в CSV-файл;
    - Если не удается найти элемент, игнорируется исключение;
12. После завершения парсинга всех товаров на странице, устанавливается значение start_card = 1 (в случае если start_card != 1 в самом начале);
13. Ожидается появление элемента ```next``` (следующая страница) и выполняется нажатие на него.
    
Это основная логика кода, которая повторяется для каждой страницы и каждой карточки товара. Каждая найденная ссылка сохраняется в CSV-файле. Если происходит ошибка при поиске элемента с ссылкой, она игнорируется, и код переходит к следующему элементу. Если алгоритм ловит блокировку, то начиная со стартовой страницы переходим к моменту где у нас была ошибка.

### 🔍📦🔗Алгоритм парсинга товара по ссылкам:
1. определяются опции для веб-драйвера Chrome и создается экземпляр драйвера:
    - устанавливаются опции Chrome для блокировки уведомлений;
    - задается стратегия загрузки страницы ```eager``` (ускоряет процесс парсинга);
    - создается экземпляр драйвера Chrome с использованием опций;
2. максимизируется окно браузера;
3. ожидается 3 секунды;
4. открывается веб-страница "https://www.eldorado.ru/d/kompyuternye-komplektuyushchie/";
5. ожидается 5 секунд;
6. удаляется элемент, который перекрывает интересующую информацию на странице;
7. выполняется нажатие на элемент для перехода на следующую страницу;
8. ожидается 2 секунды;
9. загружается CSV-файл с ссылками на товары;
11. задаются начальные значения переменных: ```start_link``` и ```start_index```;
12. происходит остановка клиента драйвера;
13. начинается цикл по ссылкам на товары из CSV-файла, начиная с start_index;
14. внутри цикла происходит открытие страницы товара по ссылке;
15. проверяется наличие ошибки ```Access to resource was blocked``` на странице. Если ошибка обнаружена, производится переход на страницу "https://www.eldorado.ru/d/kompyuternye-komplektuyushchie/", затем выполняется нажатие на элемент для перехода на следующую страницу, и снова открывается страница товара;
ожидается 2 секунды;
16. ищется рейтинг товара и количество отзывов:
    - проверяется класс элемента с рейтингом товара, и рейтинг сохраняется в переменную ```rating```;
    - получается количество отзывов, если оно доступно, и сохраняется в переменную number;
    - исключения игнорируются;
17. ищется название и цена товара:
    - название товара ищется по XPath, и результат сохраняется в переменную ```name```;
    - цена товара ищется по XPath, и результат сохраняется в переменную ```price```;
    - исключения игнорируются;
18. данные о рейтинге, количестве отзывов, названии и цене товара добавляются в словарь ```data```;
19. происходит нажатие на элемент для отображения характеристик товара.
20. происходит цикл по характеристикам товара:
    - ищется параметр характеристики и значение, и они добавляются в словарь ```data```;
    - исключения игнорируются;
21. данные о товаре добавляются в DataFrame ```data_full```;
22. dataFrame ```data_full``` сохраняется в CSV-файл;
23. выводится сообщение о завершении обработки карточки товара.
    
Данный алгоритм обработки подходит как для Eldorado так и для Citilink. Надо только заменить XPATH и убрать обработку ошибки доступа, так как у ситилинка ее нет (сразу блок ip).

### 🎉😊📝Итог
В ходе выполнения практики была поставлена задача мониторинга конкурентов, а именно парсинга данных о деятельности конкурентов в социальных сетях для отслеживания цен и реакции аудитории.
В ходе работы возникли следующие проблемы и найдены соответствующие решения:
Проблема перехода на другую страницу при парсинге. После получения данных о товаре не было возможности просто вернуться назад из-за защиты. Решением стало сперва спарсить ссылки всех товаров, затем переходить по этим ссылкам для получения нужных данных;
Блокировка IP при парсинге с сайта Citilink. Возникла блокировка доступа, которая была обойдена с помощью использования VPN;
Обработка табличных данных. Требовалось привести данные из разных таблиц к общему виду. Были проведены работы по просмотру и сравнению колонок, переименованию колонок, обработке данных, обработке категориальных признаков и приведению названий и самих структур данных к максимальной похожести;
Поиск похожих товаров. Использовались методы расстояния Левенштейна и машинного обучения с помощью метода k-ближайших соседей. Метод расстояния Левенштейна давал более точные результаты;
Кластеризация данных для каждого типа товаров. Это помогло визуализировать данные и лучше понять их распределение;
Визуализация полученных результатов. Были построены boxplot, гистограммы и диаграммы, которые позволили оценить различия в ценах, отзывах и распределении товаров среди конкурентов;
Таким образом, в результате выполнения практики была достигнута поставленная цель - мониторинг конкурентов и анализ их деятельности в социальных сетях. Благодаря данному заданию я ознакомился с парсингом данных. На практике реализовал программы на Python для парсинга данных. Попрактиковался в обработке данных. Разработанный подход к парсингу данных и определению похожих товаров позволяет получать актуальную информацию для принятия решений в бизнесе.
