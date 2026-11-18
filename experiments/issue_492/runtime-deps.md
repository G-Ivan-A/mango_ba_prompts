# Аудит зависимостей от runtime: таблица (issue #492, ФТ-1)

Сгенерировано `experiments/issue_492/audit_runtime_deps.py`; не править вручную.

- Коммит спицы: `3eda0026e6faf685d86e149c4506132d82d3ce10`.
- SHA реестра: `68ad8fcffd47439fc3051852d9a2fbbe23815855`; main runtime: `90f082330015634f3a0632cdd31ebfe1c15fd7ae`.
- Файлов просмотрено: 2548; вхождений: 2282; строк таблицы: 1166 (в области ФТ-1: 195); путей runtime: 447.

## 1. Свод по путям runtime

| Путь runtime | Источников (в области) | Потребитель | Тип ссылки | Статус | Есть на своём SHA | Есть на SHA реестра | Есть на main |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `/` | 66 (15) | валидатор, сайт, сборка | SHA (иной срез), SHA (реестр), main, корень, шаблон | защищённый | да | да | да |
| `AGENTS.md` | 14 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `README.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `contracts/c-in.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb` | 12 (0) | валидатор | SHA (иной срез), шаблон | защищённый | да | да | да |
| `docs/kb/` | 41 (3) | валидатор, сайт, сборка | SHA (иной срез), SHA (реестр), main, шаблон | защищённый | да | да | да |
| `docs/kb/MAP.json` | 57 (33) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр), main | защищённый (двойной) | да | да | да |
| `docs/kb/README.md` | 55 (32) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр), main | защищённый (двойной) | да | да | да |
| `docs/kb/USAGE.md` | 17 (12) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр), main | защищённый (двойной) | да | да | да |
| `docs/kb/api-server-client/sections/13-poryadok-perevoda-na-otvetstvennogo-sotr.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/build_map.py` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/01-stranica-avtorizacii.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/06-roboty.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/07-forma-pokupki-robotov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/08-stranica-roboty-mango-office.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/09-kartochka-robota.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/10-skripty-dlya-robotov.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/11-nastroyki-robota.md` | 2 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/12-statistika-po-skriptu-robota.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/13-analitika-po-golosovym-robotam.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/14-chat-boty.md` | 4 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/15-skripty-dlya-chat-botov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/16-nastroyki-chat-bota.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/17-statistika-po-skriptu-chat-bota.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/18-konstruktor-skriptov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/19-blok-fraza-robota.md` | 2 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/20-blok-fraza-chat-bota.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/21-blok-golos-v-tekst.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/22-blok-otpravit-sms.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/23-blok-otpravit-e-mail.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/24-blok-otpravit-http-zapros.md` | 5 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/26-blok-dobavit-tematiku.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/27-blok-perevesti-zvonok.md` | 4 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/28-blok-sravnit-znachenie.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/32-blok-raspisanie.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/36-blok-fonovye-sobytiya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/39-blok-rabota-s-pamyatyu.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/40-blok-perevesti-chat.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/43-blok-ai-assistent-dlya-chat-botov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/44-blok-ai-assistent-dlya-golosovyh-robotov.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/54-integraciya-s-api-konnektor-mango-office.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/57-peremennye.md` | 4 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/cov-robot-fil/sections/65-mnogokanalnyy-robot.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/integration-1c/sections/02-naznachenie.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-1c/sections/03-vazhnye-ogranicheniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-1c/sections/11-obrabotka-zvonkov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-1c/sections/30-osnovnye-svedeniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-amocrm/sections/60-zapis-razgovorov.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/integration-bitrix24/sections/10-obschee.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bitrix24/sections/18-bazovyy-paket.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/` | 2 (0) | валидатор | SHA (иной срез), шаблон | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/02-obzor.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/05-poryadok-deystviy.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/07-shag-2-ustanovka-softfona-mango-talker.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/10-ustanovka-sistemnyh-nastroek.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/104-obschee.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/107-kak-otpravit-klientu-soobschenie-whatsap.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/113-vhodyaschiy-zvonok.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/114-ishodyaschiy-zvonok.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/116-obschee.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/118-kak-perevesti-zvonok-s-konsultaciey.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/12-ustanovka-i-bazovye-nastroyki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/120-propuschennye-zvonki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/123-zapis-razgovorov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/13-nastoyka-podklyucheniya-k-bpmsoft.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/15-obschee.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/19-kak-nastroit-dlitelnost-uspeshno-prinyat.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/20-sozdavat-kontakt-kontragenta-lid-pri-zvo.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/24-obzor.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/35-kak-sozdat-i-nastroit-umnye-pravila.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/38-ishodyaschiy-zvonok-po-kliku-iz-bpmsoft.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/44-obschie-svedeniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/47-obschie-svedeniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/62-obzor.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/64-statusy-kontakt-centra-v-interfeyse-bpms.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/67-obzor.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/69-privyazka-zvonka-k-suschnosti-vruchnuyu.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/72-naznachenie.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/integration-bpmsoft/sections/78-opisanie-interfeysa.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/lk-vats-sso/sections/03-obschie-svedeniya.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/lk-vats-sso/sections/04-nastroyka-idp-v-lk-vats-mango-office.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/01-nachalo-raboty.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/03-registraciya-novogo-polzovatelya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/05-upravlenie-statusom.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/06-upravlenie-statusom.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/09-instrumenty-obrascheniya-ochered-obrasch.md` | 4 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/09-panel-upravleniya-telefoniey.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/10-panel-pokazateley.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/103-tegirovanie-razgovorov-v-rechevoy-analit.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/11-dashboard.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/11-panel-upravleniya-telefoniey.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/114-konstruktor-otchetov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/116-otchety.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/117-dannye.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/124-vkladka-obrabotka-zvonkov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/13-dopolnitelnye-nastroyki.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/14-prohozhdenie-kvesta-eto-poshagovoe-vypol.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/16-dashboard.md` | 4 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/17-sozdanie-i-nastroyka-vidzheta.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/18-avtomaticheskoe-raspredelenie-obrascheni.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/19-moi-obrascheniya.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/21-istoriya-obrascheniy.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/21-obrascheniya.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/22-kontrol-obrascheniy.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/23-avtomaticheskoe-raspredelenie-obrascheni.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/24-moi-obrascheniya.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/26-istoriya-obrascheniy.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/37-kontrol-sotrudnikov.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/40-zadachi.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/42-otchet-po-zadacham.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/43-plan-raboty-wfm.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/43-spisok-zadach-v-verhney-paneli.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/44-grafik-raboty.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/44-sozdanie-zadachi.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/48-nastroyki.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/50-istoriya-vyzovov.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/50-kontrol-sotrudnikov.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/51-kartochka-rabochego-dnya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/52-rabochee-vremya-sotrudnika.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/53-proizvoditelnost-sotrudnikov.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/54-proizvoditelnost-grupp.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/56-plan-raboty-wfm.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/57-grafik-raboty.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/58-planirovanie-vhodyaschih.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/58-spisok-kampaniy.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/59-otchety.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/60-obmen-smenami.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/61-dobavlenie-kampanii.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/61-nastroyki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/62-kartochka-kampanii.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/63-istoriya-vyzovov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/64-obsluzhivanie-vhodyaschih-vyzovov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/65-propuschennye-vyzovy.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/68-kontakty-adresnaya-kniga.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/69-sotrudniki.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/70-nastroyka-poley.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/72-ishodyaschiy-obzvon.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/73-tekstovye-rassylki.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/74-spisok-kampaniy.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/74-tekstovye-rassylki.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/76-nastroyka-avtomaticheskih-deystviy.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/77-biznes-analitika.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/77-dobavlenie-kampanii.md` | 4 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/78-gruppa-otchetov-prodazhi.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/78-kartochka-kampanii.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/79-gruppa-otchetov-obsluzhivanie.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-cc-manual/sections/80-skripty.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/82-sozdanie-import-eksport-skripta.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/83-statistika.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/85-sotrudniki.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/87-chaty.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/89-tekstovye-rassylki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-cc-manual/sections/96-rechevaya-analitika.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/index.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/02-vhod-v-lichnyy-kabinet.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/06-panel-licevogo-scheta.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/101-zakladka-nomera.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/102-zakladka-nomera.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/103-zakladka-nastroyki-priema-zvonkov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/104-golosovoe-menyu-i-raspredelenie-zvonkov.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/105-golosovoe-menyu-i-raspredelenie-zvonkov.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/105-nastroyki-dlya-vhodyaschih-liniy.md` | 4 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/106-dopolnitelnye-nastroyki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/106-nastroyki-dlya-vhodyaschih-liniy.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/107-dopolnitelnye-nastroyki.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/108-nastroyki-dozvona-i-soobscheniy-po-umolc.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/109-nastroyki-dozvona-i-soobscheniy-po-umolc.md` | 6 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/109-pereadresaciya-po-nomeru-klienta.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/110-chernyy-belyy-spisok.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/111-chernyy-belyy-spisok.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/112-rabota-s-sotrudnikami.md` | 5 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/113-vkladka-kartochka.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/114-vkladka-telefoniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/115-vkladka-telefoniya.md` | 1 (0) | — | SHA (реестр) | свободный | да | да | да |
| `docs/kb/mango-lk-manual/sections/117-vkladka-avtosekretar.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/118-rabota-s-gruppami.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/119-vkladka-parametry-gruppy.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/120-vkladka-sotrudniki-i-priem-vyzovov.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/121-vkladka-ochered-vyzovov.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/121-vkladka-sotrudniki-i-priem-vyzovov.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/122-roboty.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/124-statistika-i-monitoring.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/126-nagruzka-po-chasam.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/127-pokazateli-obsluzhivaniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/129-istoriya-vyzovov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/130-vse-vyzovy.md` | 5 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/131-propuschennye-vyzovy.md` | 4 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/132-propuschennye-vyzovy.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/134-zapis-razgovorov.md` | 5 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/135-zapis-razgovorov.md` | 8 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/135-zapisannye-razgovory.md` | 4 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/135-zapisi-razgovorov.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | нет | нет | нет |
| `docs/kb/mango-lk-manual/sections/136-zapisannye-razgovory.md` | 3 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/137-rezhimy-zapisi.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/138-nastroyki.md` | 5 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/138-rezhimy-zapisi.md` | 8 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/139-eksport.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/139-nastroyki.md` | 10 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/140-kontakt-centr.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/141-kontakt-centr.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/143-bitriks-24.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/145-golosovye-soobscheniya.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/145-zakaz-zvonka.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/148-analitika.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/151-otchet-propuschennye-zvonki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/152-otchet-prichiny-propuschennyh-zvonkov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/153-otchet-vremya-ozhidaniya.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/155-otchet-kolichestvo-perezvonov-po-propusc.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/159-otchet-kachestvennye-zvonki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/161-otchet-ishodyaschiy-obzvon.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/165-otchet-kolichestvo-propuschennyh-vyzovov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/168-otchet-skolko-klienty-gotovy-zhdat-na-li.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/171-otchet-srednyaya-prodolzhitelnost.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/172-otchet-vremya-ozhidaniya-otveta.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/175-otchet-skolko-zvonkov-trebuetsya-klientu.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/176-otchet-raspredelenie-zvonkov-po-punktam.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/177-otchet-raspredelenie-zvonkov-po-punktam.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/179-tekstovye-kommunikacii.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/185-kod-dlya-sayta.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/186-nastroyka-kanalov-kommunikacii.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/189-chat-na-sayte.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/190-vkontakte.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/191-whatsapp.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/192-telegram.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/193-max.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/193-telegram.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/194-max.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/195-nazanachenie-kanala-max.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/197-poluchenie-api-tokena-max.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/201-5-priem-i-obrabotka-obrascheniy.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/202-avtomaticheskie-otvety.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/204-nerabochee-vremya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/207-klientskoe-prilozhenie.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/208-e-mail.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/210-avito-rabota.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/212-chat-bot-dlya-grupp-kanalov-tekstovye-ko.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/23-blok-5-nastroyka-ishodyaschih-vyzovov.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/234-wallboard.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/238-kontrol-kachestva.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/246-statistika.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/249-etiketka-i-mav.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/249-etiketka.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/250-etiketka.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/252-karusel-nomerov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/254-sozdanie-karuseli.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/256-dobavlenie-nomerov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/272-uchetnye-zapisi-sip.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/276-audiofayly.md` | 7 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/277-audiofayly.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/278-nastroyka.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/279-nastroyka.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/28-dokumenty.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/280-zhurnal-deystviy.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/287-nastroyka-prav-dostupa-roli.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/288-dostup-k-ii-instrumentam-kontakt-centra.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/291-bezopasnost-pro.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/299-oblachnoe-hranilische.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/300-oblachnoe-hranilische.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/303-avtoperezvon.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/304-avtoperezvon.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/304-prochie.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/305-obschie-nastroyki.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/307-upravlenie-uslugami.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/308-integracii.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/308-podklyuchit-integraciyu.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/311-api-konnektor.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/49-vkladka-podderzhka.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/50-kontakty-personalnogo-menedzhera.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/51-bystrye-kanaly-svyazi.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/52-napisat-v-tehpodderzhku.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/53-napisat-v-tehpodderzhku.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/57-rabota-so-statusami.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/58-kartochka-obrascheniya.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/60-produkt-virtualnaya-ats.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/70-prilozhenie-lichnyy-kabinet.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/73-navigacionnaya-panel.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/74-smena-versii-i-tarifa-produkta.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/76-nomera-mango-office.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/mango-lk-manual/sections/78-nomera-drugih-operatorov.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mango-lk-manual/sections/99-obrabotka-zvonkov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | нет | нет |
| `docs/kb/maps/mango-lk-manual.json` | 2 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/maps/mango-lk-manual.toc.tsv` | 3 (0) | валидатор, сайт | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/maps/mtalker--windows-mac-working.json` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/maps/mtalker--windows-mac-working.toc.tsv` | 2 (0) | валидатор, сайт | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/maps/vpbx-api.toc.tsv` | 1 (0) | валидатор, сайт | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/04-podderzhivaemye-kanaly-kommunikacii.md` | 2 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/05-princip-tekstovyh-kommunikaciy-s-kliento.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/08-vvedenie-v-api.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/26-obekt-message.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/39-otpravit-soobschenie-operatora-k-klientu.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/40-zagruzka-istorii-chata.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/47-soobschenie-operatora-dostavleno-klientu.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/48-soobschenie-operatora-prochitano-kliento.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/58-priem-i-obrabotka-obrascheniy-klienta.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mdialogi-api/sections/69-istoriya-dokumenta.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/android-user-guide/sections/02-obzor.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/android-user-guide/sections/16-kak-pozvonit-ili-otpravit-sms-na-proizvo.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/android-user-guide/sections/21-upravlenie-audio-zvonkom.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/android-user-guide/sections/35-obschie-svedeniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/android-user-guide/sections/36-opisanie-elementov-interfeysa-chata-kana.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/android-user-guide/sections/47-posmotret-istoriyu-soobscheniy-v-chate.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/android-user-guide/sections/62-opisanie-zhurnala-vyzovov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/android-user-guide/sections/96-uvedomleniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-admin/sections/11-vybor-ishodyaschego-nomera.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-settings/sections/26-nastroyka-otpravki-na-e-mail.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/02-obzor.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/108-zapis-razgovora.md` | 3 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/117-obschie-svedeniya.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/125-obschie-svedeniya.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/136-ispolzovat-vneshniy-telefon.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/23-o-chatah-v-mtalker.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/57-kak-pozvonit.md` | 7 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/58-kak-prinyat-vhodyaschiy-audio-zvonok.md` | 1 (0) | — | SHA (реестр) | свободный | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/59-zakaz-obratnogo-zvonka.md` | 3 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/60-kak-dobavit-tretego-uchastnika-v-zvonok.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/63-perevod-vyzova-na-drugogo-sotrudnika.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/67-zapis-razgovora-obschie-svedeniya.md` | 8 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/mtalker/windows-mac-working/sections/68-soobschenie-vnimanie-zvonok-byl-otpravle.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/02-kak-podklyuchit-modul-kontrol-kachestva.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/05-nastroyka-blankov-ocenki.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/06-sozdanie-blanka-ocenki.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/08-nastroyka-shkaly-ocenok-i-vesa-kriteriev.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/09-nastroyka-apellyacii.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/13-ocenka-zvonkov.md` | 2 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/14-ocenka-chatov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/15-randomayzer.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/17-nastroyka-pravil-postzvonkovoy-ocenki.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/18-nastroyka-uvedomleniy-o-postzvonkovyh-oc.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/20-prosmotr-i-skachivanie-zapisey.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/23-ocenka-kachestva-v-chatah.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/26-dinamika-ocenok.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/27-svodnaya-statistika.md` | 2 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/29-apellyacii.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/30-kak-sotrudniku-podat-apellyaciyu.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/32-rechevaya-analitika.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/38-nastroyki-raspoznavaniya-zapisey.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/quality-management/sections/42-ii-tegirovanie.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/rolevaya-model-vats/sections/01-obschie-svedeniya.md` | 4 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/rolevaya-model-vats/sections/03-upravlenie-rolyami.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/rolevaya-model-vats/sections/11-nastroyka-prav-dostupa-roli.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/rolevaya-model-vats/sections/12-gibkaya-nastroyka-prav-dostupa-s-uchetom.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/rolevaya-model-vats/sections/15-vybor-podkontrolnyh-grupp.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/sip-trunk/sections/01-terminy-i-opredeleniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/sip-trunk/sections/02-chto-takoe-sip-trunk.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/sip-trunk/sections/08-nastroyka.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/sip-trunk/sections/13-rezervirovanie.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/offline-scoring/sections/34-zagruzit-vruchnuyu.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/speech-analytics/offline-scoring/sections/36-vse-razgovory.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/speech-analytics/user-guide/sections/01-obschie-svedeniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/user-guide/sections/12-ii-pomoschniki.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/speech-analytics/user-guide/sections/30-predustanovlennye-tematiki.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/speech-analytics/user-guide/sections/39-moi-otchety.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/speech-analytics/user-guide/sections/53-statistika.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/02-obschie-svedeniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/04-podklyuchenie-v-demo-rezhime.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/05-podklyuchenie-uslugi-v-platnom-rezhime.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/08-nastroyki-raspoznavaniya-zapisey.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/11-ii-konspekty.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/12-ii-tegirovanie.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/14-chto-eto-takoe-i-zachem-nuzhno.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/16-nastroyka-ii-pomoschnika.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/25-polya-formy-modulya-poiska-v-zapisyah-ra.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/26-proslushivanie-zapisey.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/27-tegirovanie-razgovorov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/30-klyuchevye-slova.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/35-predustanovlennye-tematiki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/36-zayavki-na-uluchshenie-kachestva-raspozn.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/38-ii-tematiki.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/39-oflayn-skoring.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/40-oflaynovye-zapisi.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/46-nastroyki-api.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/47-zagruzit-vruchnuyu.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/51-otchety.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/56-blok-tablicy-razgovory-detalizaciya.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/57-detalizaciya-razgovorov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/60-blok-vizualizaciy.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/63-analiz-po-chek-listam.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/64-konstruktor-chek-listov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/65-statistika.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/67-lovec-insaytov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/68-blok-parametrov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/70-pokazateli-otchetov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/71-roli-i-prava-dostupa.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/speech-analytics/vats-offline-scoring/sections/72-integraciya-rechevoy-analitiki-so-storon.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/01-opredeleniya-i-sokrascheniya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/03-naznachenie.md` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/04-trebovaniya-sovmestimosti-i-spisok-podde.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/102-obschee.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/106-dobavlenie-nomera-v-ch-b-spisok-vats.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/14-api-vats.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/158-upravlenie-zadachey-na-avtoperezvon.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/159-sozdanie-zadachi-na-avtoperezvon.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/169-smena-statusa-sessii-polzovatelya.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/170-smena-statusa-polzovatelya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/174-izmenenie-statusa-polzovatelya.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/186-obschee.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/191-opisanie-zaprosa-na-sozdanie-kampanii-io.md` | 2 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/192-obnovlenie-kampanii.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/193-dobavlenie-neskolkih-zadaniy-v-kampaniyu.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/196-ostanovka-kampanii.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/199-poluchenie-informacii-o-zadache-kampanii.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/20-o-parametre-sign.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/210-poluchenie-dannyh-kontakt-centra-dlya-zv.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/214-rabota-s-obrascheniyami-v-kontakt-centre.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/26-obschee.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/27-uvedomlenie-o-vyzove.md` | 4 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/28-uvedomlenie-o-rezultate-otpravki-sms.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/29-uvedomlenie-o-zapisi-razgovora.md` | 4 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/32-uvedomlenie-o-zavershenii-vyzova.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/36-iniciirovanie-vyzova-ot-imeni-sotrudnika.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/39-otpravka-sms.md` | 2 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/40-vklyuchenie-zapisi-razgovora.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/41-vklyuchenie-vosproizvedeniya-zvukovogo-f.md` | 4 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/42-marshrutizaciya-vyzova.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/55-api-statistika.md` | 3 (0) | валидатор | SHA (иной срез), SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/58-poluchenie-statistiki-vyzovov.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/63-api-zapisi-razgovorov-rechevaya-analitik.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/64-poluchenie-zapisi-razgovora-posredstvom.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/65-poluchenie-zapisi-razgovora-posredstvom.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/66-pryamaya-ssylka-na-zapis-razgovora-s-avt.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/68-poluchenie-spiska-rasshifrovok-raspoznan.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/70-zapros-zapisey-s-rasshifrovkami-zvonkov.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/76-api-konfiguraciya.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/77-zapros-spiska-sotrudnikov-vats.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/79-dobavit-gruppu.md` | 2 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/84-poluchenie-spiska-melodiy-i-zvukovyh-soo.md` | 2 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/vpbx-api/sections/88-sozdat-sotrudnika.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `docs/kb/wallboard/sections/01-nachalo-raboty.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `docs/kb/wallboard/sections/13-pokazateli-proizvoditelnosti-gruppy-zvon.md` | 1 (0) | валидатор | SHA (реестр) | защищённый | да | да | да |
| `evaluation/g-human-checklist.md` | 4 (3) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр) | защищённый (двойной) | да | да | да |
| `evaluation/validate-package.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `golden/cases-analytics-reporting.yaml` | 3 (3) | валидатор, модель, сайт | SHA (реестр) | защищённый (двойной) | да | да | да |
| `golden/cases-voice-ucaas.yaml` | 3 (3) | валидатор, модель, сайт | SHA (реестр) | защищённый (двойной) | да | да | да |
| `golden/cases.yaml` | 12 (4) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр), клон | защищённый (двойной) | да | да | да |
| `golden/gs-cc-01-queue-overflow.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `golden/gs-cc-neg-03-sla-vs-aht.md` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `routes/rg-bcreq-v1.yaml` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `skills/` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `taxonomy/domain-glossary-analytics-reporting.yaml` | 6 (6) | валидатор, модель, сайт | SHA (реестр) | защищённый (двойной) | да | да | да |
| `taxonomy/domain-glossary-voice-ucaas.yaml` | 10 (6) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр) | защищённый (двойной) | да | да | да |
| `taxonomy/domain-glossary.yaml` | 6 (6) | валидатор, модель, сайт | SHA (реестр) | защищённый (двойной) | да | да | да |
| `taxonomy/mango-products.yaml` | 19 (8) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр), клон | защищённый (двойной) | да | да | да |
| `taxonomy/processes.yaml` | 3 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `taxonomy/products.yaml` | 65 (34) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр), main, клон | защищённый (двойной) | да | да | да |
| `taxonomy/projections.yaml` | 1 (0) | валидатор | SHA (иной срез) | защищённый | да | да | да |
| `taxonomy/source-tiers.yaml` | 26 (22) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр) | защищённый (двойной) | да | да | да |
| `templates/bcreq-skeleton.md` | 8 (5) | валидатор, модель, сайт | SHA (иной срез), SHA (реестр) | защищённый (двойной) | да | да | да |

## 2. Таблица ФТ-1: область аудита

Файл-источник → путь runtime → тип ссылки → потребитель → статус.

| Файл-источник | Строки | Путь runtime | Тип ссылки | Потребитель | Основание | Статус |
| --- | --- | --- | --- | --- | --- | --- |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 295,531 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 294 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 531 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 532 | `taxonomy/domain-glossary-analytics-reporting.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 532 | `taxonomy/domain-glossary-voice-ucaas.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 532 | `taxonomy/domain-glossary.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 267 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-context-understanding-stepwise.md` | 533 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 216 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 215 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-in-understanding-oneshot.md` | 188 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-intake-questionnaire-stepwise.md` | 236 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 213,422 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 212 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 422 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 423,429 | `taxonomy/mango-products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 185,423 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/archive/a-in-v2.7.0/bcreq-products-impact-analysis-stepwise.md` | 424 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 430 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 429 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-constitution-governance-oneshot.md` | 402 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-constraints-documentation-stepwise.md` | 165 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-constraints-documentation-stepwise.md` | 164 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-constraints-documentation-stepwise.md` | 137 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-context-understanding-stepwise.md` | 362 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-context-understanding-stepwise.md` | 361 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-context-understanding-stepwise.md` | 334 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-core-documentation-oneshot.md` | 263 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-core-documentation-oneshot.md` | 262 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-core-documentation-oneshot.md` | 235 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-extra-risk-analysis-stepwise.md` | 165 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-extra-risk-analysis-stepwise.md` | 164 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-extra-risk-analysis-stepwise.md` | 137 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-fr-documentation-stepwise.md` | 293 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-fr-documentation-stepwise.md` | 292 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-fr-documentation-stepwise.md` | 265 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-in-understanding-oneshot.md` | 292 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-in-understanding-oneshot.md` | 291 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-in-understanding-oneshot.md` | 264 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-nfr-documentation-stepwise.md` | 164 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-nfr-documentation-stepwise.md` | 163 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-nfr-documentation-stepwise.md` | 136 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 240 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 239 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-orr-solution-design-stepwise.md` | 212 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 280 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 279 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-products-impact-analysis-stepwise.md` | 252 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-review-validation-oneshot.md` | 182 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-review-validation-oneshot.md` | 181 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-review-validation-oneshot.md` | 154 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | 159 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | 158 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-scenarios-modeling-oneshot.md` | 131 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-uc-modeling-stepwise.md` | 200 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-uc-modeling-stepwise.md` | 199 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-uc-modeling-stepwise.md` | 172 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 211 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 210 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/bcreq-work-solution-design-oneshot.md` | 183 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 441 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 440 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 413 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 640 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constitution-governance-oneshot.md` | 639 | `templates/bcreq-skeleton.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 174,339 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 173 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 339 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 146 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-constraints-documentation-stepwise.md` | 340 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 371,607 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 370 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 607 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 608 | `taxonomy/domain-glossary-analytics-reporting.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 608 | `taxonomy/domain-glossary-voice-ucaas.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 608 | `taxonomy/domain-glossary.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 343 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-context-understanding-stepwise.md` | 609 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 174 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 173 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 146 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-extra-risk-analysis-stepwise.md` | 353 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 302,474 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 301 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 474 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 274 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-fr-documentation-stepwise.md` | 476 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-intake-questionnaire-stepwise.md` | 313 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 173 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 172 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 145 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-nfr-documentation-stepwise.md` | 339 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 249,421 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 248 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 421 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 221 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-orr-solution-design-stepwise.md` | 422 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 289,498 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 288 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 498 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 499,505 | `taxonomy/mango-products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 261,499 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-products-impact-analysis-stepwise.md` | 500 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 287 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-release-readiness-oneshot.md` | 286 | `templates/bcreq-skeleton.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 191 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 190 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 416 | `evaluation/g-human-checklist.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 414 | `golden/cases-analytics-reporting.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 414 | `golden/cases-voice-ucaas.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 414 | `golden/cases.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 163 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 415 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-review-validation-oneshot.md` | 413 | `templates/bcreq-skeleton.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 168 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 167 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 140 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-scenarios-modeling-oneshot.md` | 341 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 209 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 208 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 181 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/bcreq-uc-modeling-stepwise.md` | 391 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 381,617 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 380 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 617 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 618 | `taxonomy/domain-glossary-analytics-reporting.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 618 | `taxonomy/domain-glossary-voice-ucaas.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 618 | `taxonomy/domain-glossary.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 353 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-context-understanding-system.md` | 619 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-intake-questionnaire-system.md` | 324 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 299,508 | `docs/kb/MAP.json` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 298 | `docs/kb/README.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 508 | `docs/kb/USAGE.md` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 509,515 | `taxonomy/mango-products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 271,509 | `taxonomy/products.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `prompts/drafts/system/bcreq-products-impact-analysis-system.md` | 510 | `taxonomy/source-tiers.yaml` | SHA (реестр) | модель, сайт, валидатор | текст промпта; ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_430_runtime_refs.py | защищённый (двойной) |
| `scripts/build_bcreq_step_prompts.py` | 57 | `/` | main | сборка | генератор/снимок | защищённый |
| `scripts/kb/runtime_snapshot.py` | 15 | `/` | корень | сайт, сборка | ссылка в site/data/*.json; генератор/снимок | защищённый |
| `scripts/kb/runtime_snapshot.py` | 20,42,48 | `docs/kb/` | SHA (иной срез) | сборка | генератор/снимок | защищённый |
| `scripts/test_issue_361_kb_migration.py` | 11 | `docs/kb/` | main | валидатор | код валидатора | защищённый |
| `scripts/validate_issue_430_runtime_refs.py` | 136 | `/` | корень | сайт, валидатор | ссылка в site/data/*.json; код валидатора | защищённый |
| `scripts/validate_issue_430_runtime_refs.py` | 198 | `/` | шаблон | сайт, валидатор | ссылка в site/data/*.json; код валидатора | защищённый |
| `scripts/validate_issue_430_runtime_refs.py` | 51 | `taxonomy/mango-products.yaml` | клон | валидатор | код валидатора | защищённый |
| `scripts/validate_issue_434_runtime_tasks.py` | 374 | `/` | шаблон | сайт, валидатор | ссылка в site/data/*.json; код валидатора | защищённый |
| `scripts/validate_issue_434_runtime_tasks.py` | 347,358,677 | `golden/cases.yaml` | клон | валидатор | код валидатора | защищённый |
| `scripts/validate_issue_434_runtime_tasks.py` | 332,674 | `taxonomy/mango-products.yaml` | клон | валидатор | код валидатора | защищённый |
| `scripts/validate_issue_434_runtime_tasks.py` | 671 | `taxonomy/products.yaml` | клон | валидатор | код валидатора | защищённый |
| `site/app.js` | 1785 | `docs/kb/` | main | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3392,3392,3393,3393,3484,3485… | `docs/kb/MAP.json` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3392,3393,3484,3485,3642,3643… | `docs/kb/README.md` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3392,3393,3642,3643 | `docs/kb/USAGE.md` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3392,3393 | `taxonomy/domain-glossary-analytics-reporting.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3392,3393 | `taxonomy/domain-glossary-voice-ucaas.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3392,3393 | `taxonomy/domain-glossary.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3642,3642,3643,3643 | `taxonomy/mango-products.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3392,3393,3484,3485,3642,3642… | `taxonomy/products.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/prompts.json` | 3392,3393,3555,3556,3642,3643 | `taxonomy/source-tiers.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 231,296,296,314,314,341… | `docs/kb/MAP.json` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 231,296,314,341,359,395… | `docs/kb/README.md` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 296,314,341,359,395,503… | `docs/kb/USAGE.md` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 647 | `evaluation/g-human-checklist.md` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 647 | `golden/cases-analytics-reporting.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 647 | `golden/cases-voice-ucaas.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 647 | `golden/cases.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 296,314 | `taxonomy/domain-glossary-analytics-reporting.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 296,314 | `taxonomy/domain-glossary-voice-ucaas.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 296,314 | `taxonomy/domain-glossary.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 341,341,359,359 | `taxonomy/mango-products.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 231,296,314,341,341,359… | `taxonomy/products.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 231,258,269,296,314,341… | `taxonomy/source-tiers.yaml` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/data/test-kit.json` | 231,647,676 | `templates/bcreq-skeleton.md` | SHA (реестр) | сайт | исходник сайта | защищённый |
| `site/index.html` | 59 | `/` | корень | сайт | исходник сайта | защищённый |
| `standards/bcreq-flow-glossary.md` | 366 | `/` | SHA (реестр) | валидатор | читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_427_rfc.py, validate_issue_430_runtime_refs.py | защищённый |
| `standards/bcreq-runtime-references.md` | 9,51,203 | `/` | корень | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 53,223 | `/` | корень | валидатор | читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 53,106,186,187,218,220… | `/` | корень | валидатор | читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 128,149 | `/` | шаблон | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 218 | `/` | корень | валидатор | читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 218 | `/` | корень | валидатор | читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 218 | `/` | корень | валидатор | читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 220,221,222 | `/` | корень | валидатор | читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 76 | `docs/kb/MAP.json` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 76 | `docs/kb/USAGE.md` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 83 | `evaluation/g-human-checklist.md` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 80 | `golden/cases-analytics-reporting.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 80 | `golden/cases-voice-ucaas.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 80 | `golden/cases.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 81 | `taxonomy/domain-glossary-analytics-reporting.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 81 | `taxonomy/domain-glossary-voice-ucaas.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 81 | `taxonomy/domain-glossary.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 77 | `taxonomy/mango-products.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 77 | `taxonomy/products.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 82 | `taxonomy/source-tiers.yaml` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |
| `standards/bcreq-runtime-references.md` | 78 | `templates/bcreq-skeleton.md` | SHA (реестр) | сайт, валидатор | ссылка в site/data/*.json; читает validate_issue_265_hub_sync.py, validate_issue_409_audit_artifacts.py, validate_issue_430_runtime_refs.py, validate_issue_434_runtime_tasks.py | защищённый |

## 3. Вне области ФТ-1 (справочно)

Прогоны, RFC, анализы, эксперименты и прочее фиксируют срез на свою дату.

| Файл-источник | Вхождений | Путей | Типы ссылок | Потребитель | Статус |
| --- | --- | --- | --- | --- | --- |
| `CHANGELOG.md` | 3 | 2 | main, корень | валидатор | защищённый |
| `CONTRIBUTING.md` | 1 | 1 | main | валидатор | защищённый |
| `docs/adr/2026-10-adr-013-product-portal-mapping.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `docs/analysis/2026-10-28-bcreq-evolution-failure-analysis.md` | 2 | 2 | SHA (иной срез) | валидатор | защищённый |
| `docs/analysis/2026-10-31-follow-up-tasks.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `docs/analysis/2026-10-31-requirements-evolution.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `docs/analysis/2026-10-31-strategic-documents-proposal.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `docs/analysis/2026-11-01-standards-page-risk-review.md` | 2 | 1 | корень | валидатор, сайт | защищённый |
| `docs/analysis/2026-11-04-bl-156-157-readiness-check.md` | 2 | 1 | SHA (иной срез), корень | валидатор, сайт | защищённый |
| `docs/analysis/2026-11-04-bl-156-readiness-check-444.md` | 2 | 1 | SHA (иной срез), корень | валидатор | защищённый |
| `docs/audit/2026-10-31-repository-audit.md` | 2 | 2 | SHA (иной срез) | валидатор | защищённый |
| `docs/rfc/2026-10-repository-modernization.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `docs/rfc/2026-10-standards-page.md` | 3 | 3 | SHA (иной срез) | валидатор | защищённый |
| `docs/rfc/2026-11-bcreq-flow-processes-prompts.md` | 5 | 3 | SHA (иной срез), шаблон | валидатор | защищённый |
| `docs/rfc/2026-11-runtime-product-catalog-golden-set.md` | 38 | 16 | SHA (иной срез), SHA (реестр), корень, шаблон | валидатор, сайт | защищённый |
| `docs/taxonomy/README.md` | 3 | 3 | SHA (иной срез) | валидатор | защищённый |
| `docs/taxonomy/products.json` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `docs/taxonomy/routing-examples.json` | 6 | 2 | SHA (иной срез) | — | свободный |
| `experiments/issue_363/generate_run.py` | 2 | 2 | шаблон | — | свободный |
| `experiments/issue_365/generate_run.py` | 2 | 2 | шаблон | — | свободный |
| `experiments/issue_367/generate_run.py` | 2 | 2 | шаблон | — | свободный |
| `experiments/issue_369/generate_run.py` | 2 | 2 | шаблон | — | свободный |
| `experiments/issue_371/generate_run.py` | 2 | 2 | шаблон | — | свободный |
| `experiments/issue_373_golden_set.py` | 2 | 1 | шаблон | — | свободный |
| `experiments/issue_375_golden_set.py` | 2 | 1 | шаблон | — | свободный |
| `experiments/issue_378_golden_set.py` | 2 | 1 | шаблон | — | свободный |
| `experiments/issue_382/generate_run.py` | 3 | 3 | шаблон | — | свободный |
| `experiments/issue_395/source-notes.md` | 4 | 4 | main | валидатор | защищённый |
| `experiments/issue_397/build_report_refs.py` | 1 | 1 | корень | сайт | защищённый |
| `experiments/issue_397/evidence.json` | 3 | 2 | main, корень | сайт | защищённый, свободный |
| `experiments/issue_397/evidence.md` | 3 | 2 | main, корень | валидатор, сайт | защищённый |
| `experiments/issue_399/build.py` | 1 | 1 | SHA (иной срез) | — | свободный |
| `experiments/issue_399/route.py` | 1 | 1 | SHA (иной срез) | — | свободный |
| `experiments/issue_420/site-v2/content.py` | 1 | 1 | корень | сайт | защищённый |
| `experiments/issue_427/issue-body.md` | 2 | 2 | main, корень | валидатор, сайт | защищённый |
| `experiments/issue_430/pr-body.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_432/pr-body.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_432/pr431-body.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_434/pr-body.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_438/run0080/post-run-deltas.json` | 14 | 7 | SHA (иной срез) | — | свободный |
| `experiments/issue_438/task-statement.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_442/task-statement.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_444/bl156a_prompt_changes.py` | 1 | 1 | main | — | свободный |
| `experiments/issue_444/mutation_check.py` | 2 | 1 | SHA (иной срез), шаблон | — | свободный |
| `experiments/issue_444/pr-body.md` | 2 | 1 | корень | валидатор | защищённый |
| `experiments/issue_444/task-statement.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_446/run0083/executor-instruction.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_446/task-statement.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_448/task-statement.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_450/task-statement.md` | 1 | 1 | корень | валидатор | защищённый |
| `experiments/issue_454/run0089/executor-instruction.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_458/executor-instruction.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `experiments/issue_458/finalize.py` | 1 | 1 | корень | сайт | защищённый |
| `experiments/issue_474/recording-observation.json` | 1 | 1 | SHA (реестр) | — | свободный |
| `experiments/issue_474/retrieval-smoke.md` | 1 | 1 | SHA (реестр) | валидатор | защищённый |
| `experiments/issue_476/README.md` | 1 | 1 | main | валидатор | защищённый |
| `experiments/issue_482/generate_run.py` | 2 | 2 | шаблон | — | свободный |
| `experiments/issue_484/generate_run.py` | 1 | 1 | шаблон | — | свободный |
| `experiments/issue_484/ssot.py` | 1 | 1 | шаблон | — | свободный |
| `experiments/issue_486/generate_run.py` | 1 | 1 | шаблон | — | свободный |
| `kb/README.md` | 1 | 1 | main | валидатор | защищённый |
| `kb/USAGE.md` | 1 | 1 | main | валидатор | защищённый |
| `kb/processed/README.md` | 2 | 1 | SHA (иной срез), main | валидатор | защищённый |
| `kb/sources/README.md` | 1 | 1 | main | валидатор | защищённый |
| `pr-ops/BACKLOG.md` | 4 | 1 | корень | валидатор | защищённый |
| `pr-ops/backlog-ba-model.md` | 3 | 1 | корень | валидатор | защищённый |
| `runs/2026/RUN-0068/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0068/outputs/L0-feasibility-assessment-1114.md` | 21 | 15 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0069/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0069/outputs/L0-feasibility-assessment-1114-2.md` | 52 | 32 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0070/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0070/outputs/L0-feasibility-assessment-1115.md` | 276 | 106 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0071/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0071/outputs/L0-feasibility-assessment-1116.md` | 218 | 105 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0072/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0072/outputs/L0-feasibility-assessment-1117.md` | 113 | 75 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0073/inputs/README.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0073/logs/kb-verification.md` | 8 | 8 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0073/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0073/outputs/error-statistics.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0073/outputs/golden-set-candidates.md` | 2 | 2 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0073/outputs/how-not-to-do-by-product.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0073/outputs/incident-register.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0073/outputs/runtime-improvements.md` | 4 | 3 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0073/outputs/section-prompts.md` | 1 | 1 | шаблон | валидатор | защищённый |
| `runs/2026/RUN-0074/inputs/README.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0074/logs/kb-verification.md` | 8 | 8 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0074/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0074/outputs/error-statistics.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0074/outputs/golden-set-candidates.md` | 2 | 2 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0074/outputs/how-not-to-do-by-product.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0074/outputs/incident-register.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0074/outputs/runtime-improvements.md` | 4 | 3 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0075/inputs/README.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0075/logs/kb-verification.md` | 12 | 12 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0075/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0075/outputs/error-statistics.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0075/outputs/golden-set-candidates.md` | 2 | 2 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0075/outputs/how-not-to-do-by-product.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0075/outputs/incident-register.md` | 1 | 1 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0075/outputs/runtime-improvements.md` | 4 | 3 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0077/metadata.yaml` | 1 | 1 | SHA (иной срез) | — | свободный |
| `runs/2026/RUN-0077/outputs/L0-feasibility-assessment-1125.md` | 346 | 124 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0083/logs/executor-instruction.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `runs/2026/RUN-0083/outputs/P-transcript.md` | 26 | 15 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0083/outputs/T-transcript.md` | 23 | 13 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0084/inputs/prompt-A0.md` | 3 | 3 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0084/inputs/prompt-A1.md` | 3 | 3 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0084/inputs/prompt-A2.md` | 3 | 3 | SHA (иной срез) | валидатор | защищённый |
| `runs/2026/RUN-0085/inputs/prompt-A2.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0085/inputs/prompt-A3.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0086/inputs/prompt-S1-B.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0086/inputs/prompt-S1-C.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0086/inputs/prompt-S3-B.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0086/inputs/prompt-S3-C.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0086/inputs/prompt-S6-B.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0086/inputs/prompt-S6-C.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0087/inputs/prompt-B.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0087/inputs/prompt-C.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0088/logs/executor-instruction.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `runs/2026/RUN-0088/outputs/document/current.json` | 31 | 17 | SHA (реестр) | — | свободный |
| `runs/2026/RUN-0088/outputs/document/sc-input.md` | 13 | 13 | SHA (реестр) | валидатор | защищённый |
| `runs/2026/RUN-0089/logs/executor-instruction.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `runs/2026/RUN-0089/outputs/K-document.md` | 1 | 1 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0089/outputs/K-transcript.md` | 107 | 23 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0089/outputs/T-document.md` | 1 | 1 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0089/outputs/T-transcript.md` | 62 | 27 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0089/outputs/common-transcript.md` | 35 | 21 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0090/logs/executor-instruction.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `runs/2026/RUN-0090/logs/experiment-log.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `runs/2026/RUN-0090/outputs/bcreq.md` | 1 | 1 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0091/logs/executor-instruction.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `runs/2026/RUN-0091/logs/experiment-log.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `runs/2026/RUN-0091/outputs/bcreq.md` | 1 | 1 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0092/outputs/gate-c1-01-dialogue.md` | 1 | 1 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0092/outputs/gate-in-01-dialogue.md` | 3 | 3 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0092/outputs/sc-01-dialogue.md` | 12 | 11 | SHA (реестр) | валидатор, сайт | защищённый |
| `runs/2026/RUN-0093/inputs/README.md` | 1 | 1 | SHA (реестр) | валидатор | защищённый |
| `runs/2026/RUN-0093/metadata.yaml` | 1 | 1 | SHA (реестр) | — | свободный |
| `runs/2026/RUN-0093/outputs/L0-feasibility-assessment-1140.md` | 63 | 35 | SHA (реестр) | валидатор | защищённый |
| `runs/2026/RUN-0094/inputs/README.md` | 1 | 1 | SHA (реестр) | валидатор | защищённый |
| `runs/2026/RUN-0094/inputs/task-statement-486.md` | 1 | 1 | корень | валидатор, сайт | защищённый |
| `runs/2026/RUN-0094/metadata.yaml` | 1 | 1 | SHA (реестр) | — | свободный |
| `runs/2026/RUN-0094/outputs/L0-feasibility-assessment-1199-2.md` | 169 | 77 | SHA (реестр) | валидатор | защищённый |
