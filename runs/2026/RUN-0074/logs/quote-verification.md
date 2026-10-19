---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/377"
related_artifacts:
  - "experiments/issue_377_verify_quotes.py"
---

# Журнал сверки цитат прогона RUN-0074

> Файл **порождён** скриптом [`experiments/issue_377_golden_set.py`](../../../../experiments/issue_377_golden_set.py) из вывода [`experiments/issue_377_verify_quotes.py`](../../../../experiments/issue_377_verify_quotes.py) — не редактируйте вручную.

Каждая цитата разметки искалась в тексте заявленной реплики экспорта после нормализации (пробелы схлопнуты, `*` и `` ` `` удалены). Текст экспорта в журнал не копируется: фиксируется SHA-256 нормализованной цитаты.

- SHA-256 экспорта: `f903e8f3991750d1ccc9cc442b66968b8637655c84613f85641db5b9e761b09a`
- Реплик в ветке: 156
- Цитат проверено: 559; не найдено в заявленной реплике: **0**
- Встречаются ещё и в других репликах: 62 (заявленная реплика входит в список найденных — привязка однозначна по номеру реплики)

| Вид цитаты | Проверено |
| --- | --- |
| `incident` | 333 |
| `incident-rule` | 8 |
| `incident-uq` | 115 |
| `negative` | 27 |
| `negative-uq` | 11 |
| `success` | 65 |

| Ссылка | Вид | Реплика | Найдена | Также в репликах | SHA-256 (нормализованной) |
| --- | --- | --- | --- | --- | --- |
| I-001 | `incident` | 0 | да | — | `147b10828d580dfc` |
| I-002 | `incident` | 0 | да | — | `c65d81b74e031709` |
| I-002 | `incident-uq` | 10 | да | — | `65f85ee8601c6707` |
| I-003 | `incident` | 0 | да | — | `c870e355b40cb207` |
| I-003 | `incident-uq` | 10 | да | — | `a3757aa3e542fa19` |
| I-004 | `incident` | 0 | да | — | `7169b4cadf66b475` |
| I-004 | `incident-uq` | 12 | да | — | `fb7c23708c52dffe` |
| I-005 | `incident` | 0 | да | — | `ccd70741887576dd` |
| I-005 | `incident-uq` | 12 | да | — | `5047c0408019fcd5` |
| I-006 | `incident` | 0 | да | — | `de2facb1b3c08873` |
| I-007 | `incident` | 0 | да | — | `5bfd814e52e0410d` |
| I-008 | `incident` | 0 | да | — | `07510f47ef7978fa` |
| I-009 | `incident` | 3 | да | — | `141d70f9ab512431` |
| I-009 | `incident-uq` | 4 | да | — | `ede8337202d13e72` |
| I-010 | `incident` | 3 | да | — | `afbdd7ae60724494` |
| I-011 | `incident` | 3 | да | — | `ce012e3495178c02` |
| I-012 | `incident` | 5 | да | — | `7ad66bd9c5851038` |
| I-012 | `incident-uq` | 12 | да | — | `5047c0408019fcd5` |
| I-013 | `incident` | 5 | да | — | `b7bad5f7ac059064` |
| I-013 | `incident-uq` | 12 | да | — | `83660adf0122b400` |
| I-014 | `incident` | 5 | да | — | `2031823ae6f1a4de` |
| I-014 | `incident-uq` | 12 | да | — | `83660adf0122b400` |
| I-015 | `incident` | 7 | да | — | `807a648176447125` |
| I-016 | `incident` | 7 | да | — | `3ca909071535f000` |
| I-016 | `incident-uq` | 8 | да | — | `af9eba0117f2ec7d` |
| I-017 | `incident` | 7 | да | — | `c6fe9022dce5ec1a` |
| I-018 | `incident` | 7 | да | — | `4b8521ae7dcf3164` |
| I-018 | `incident-uq` | 12 | да | — | `fb7c23708c52dffe` |
| I-019 | `incident` | 7 | да | — | `d6a9e899e0acecc5` |
| I-019 | `incident-uq` | 12 | да | — | `173f7163c979ee48` |
| I-020 | `incident` | 7 | да | — | `8140f2496d145dcc` |
| I-021 | `incident` | 7 | да | — | `56d60df9df03e3c6` |
| I-022 | `incident` | 9 | да | — | `678b5516105c2029` |
| I-022 | `incident-uq` | 10 | да | — | `a3757aa3e542fa19` |
| I-023 | `incident` | 9 | да | — | `b541d93806268afb` |
| I-023 | `incident-uq` | 20 | да | — | `5516744496a24363` |
| I-024 | `incident` | 9 | да | — | `96134e9585d9fd74` |
| I-025 | `incident` | 11 | да | — | `f4d56e9d983aed72` |
| I-025 | `incident-uq` | 12 | да | — | `fb7c23708c52dffe` |
| I-026 | `incident` | 11 | да | — | `ce1666f7933b6736` |
| I-026 | `incident-uq` | 12 | да | — | `173f7163c979ee48` |
| I-027 | `incident` | 11 | да | — | `f0c101f59b6477f1` |
| I-027 | `incident-uq` | 12 | да | — | `010436229447e037` |
| I-028 | `incident` | 11 | да | — | `3fd2af84709dcc9e` |
| I-028 | `incident-uq` | 12 | да | — | `7e6d2d7edb6ccfdf` |
| I-029 | `incident` | 11 | да | — | `9d9fd11e30fc588b` |
| I-029 | `incident-uq` | 12 | да | — | `fcbcf278c0ee314e` |
| I-030 | `incident` | 11 | да | — | `33cb3ae24ba6db04` |
| I-031 | `incident` | 11 | да | — | `1e4d773168dc457f` |
| I-032 | `incident` | 11 | да | — | `7f035088e647763e` |
| I-032 | `incident-uq` | 12 | да | — | `91f256daadfdd76b` |
| I-033 | `incident` | 11 | да | — | `5e648875b3e17c23` |
| I-033 | `incident-uq` | 12 | да | — | `fcbcf278c0ee314e` |
| I-034 | `incident` | 11 | да | — | `675dc2e67995de93` |
| I-035 | `incident` | 13 | да | — | `f260e9920c2f142e` |
| I-035 | `incident-uq` | 14 | да | — | `0aba427a156ee1b7` |
| I-036 | `incident` | 13 | да | — | `e2db5cc7da4cbbce` |
| I-036 | `incident-uq` | 14 | да | — | `7393a32d6b6d004a` |
| I-037 | `incident` | 13 | да | — | `41014cb5918c7c50` |
| I-037 | `incident-uq` | 14 | да | 70, 92, 94, 98, 106, 110, 134, 148, 154 | `9da835213d94f686` |
| I-038 | `incident` | 13 | да | — | `56e6fd488b76c822` |
| I-038 | `incident-uq` | 14 | да | 70, 92, 94, 98, 106, 110, 134, 148, 154 | `e5fad3357eb8363b` |
| I-039 | `incident` | 13 | да | — | `c7e2a75f556b7833` |
| I-040 | `incident` | 13 | да | — | `2b725308dc81e887` |
| I-040 | `incident-uq` | 14 | да | 70, 92, 94, 98, 106, 110, 112 | `a2a71fc2905f85a5` |
| I-041 | `incident` | 15 | да | — | `9d4a205c32ddd6e7` |
| I-042 | `incident` | 15 | да | 16 | `b87de05ed75ab639` |
| I-042 | `incident-uq` | 16 | да | — | `4431f4a44db4b55c` |
| I-043 | `incident` | 15 | да | — | `e6bbe75072794233` |
| I-043 | `incident-uq` | 16 | да | — | `cf45532de2ad44ee` |
| I-044 | `incident` | 15 | да | — | `e17ee07a14d285d6` |
| I-045 | `incident` | 15 | да | — | `2083e733111cf714` |
| I-045 | `incident-uq` | 16 | да | — | `5b0da4ddbfe2722c` |
| I-046 | `incident` | 15 | да | — | `05bfd79e6a53d5cf` |
| I-046 | `incident-uq` | 16 | да | — | `88c706710c919ba8` |
| I-047 | `incident` | 15 | да | — | `baaf274253e56b3a` |
| I-048 | `incident` | 17 | да | — | `52042c825e599059` |
| I-049 | `incident` | 17 | да | — | `4d7ec7cb2c9fab01` |
| I-050 | `incident` | 17 | да | — | `09a32e6579430ed1` |
| I-051 | `incident` | 17 | да | — | `6de82a82d566233c` |
| I-051 | `incident-uq` | 20 | да | — | `5516744496a24363` |
| I-052 | `incident` | 19 | да | 20 | `724911920a245c38` |
| I-052 | `incident-uq` | 20 | да | — | `12be3fd74e7ab77b` |
| I-053 | `incident` | 19 | да | — | `0f0ef3cb64b2696a` |
| I-053 | `incident-uq` | 20 | да | — | `12be3fd74e7ab77b` |
| I-054 | `incident` | 19 | да | — | `e81cee4fab7b7e6e` |
| I-054 | `incident-uq` | 20 | да | — | `68bc5b623f0b7858` |
| I-055 | `incident` | 19 | да | — | `7b41b195c0ca1cf1` |
| I-056 | `incident` | 19 | да | — | `6c72aa522821f8b1` |
| I-057 | `incident` | 21 | да | — | `d3901cd8c5dd0adb` |
| I-058 | `incident` | 21 | да | — | `e483a0212a5f0bf7` |
| I-059 | `incident` | 21 | да | — | `e483a0212a5f0bf7` |
| I-059 | `incident-uq` | 22 | да | — | `ca4c0f684a7335a7` |
| I-060 | `incident` | 21 | да | — | `64978bc5d712447c` |
| I-060 | `incident-uq` | 22 | да | — | `139b5676e9b24797` |
| I-061 | `incident` | 21 | да | — | `9936a2fc85f79a4a` |
| I-062 | `incident` | 21 | да | — | `5ac6e5aca2b545b9` |
| I-062 | `incident-uq` | 22 | да | — | `1b6d2eeff20b56d8` |
| I-063 | `incident` | 23 | да | — | `cfc3e153e67c6d76` |
| I-064 | `incident` | 23 | да | — | `b48c1dc61cd19254` |
| I-064 | `incident-uq` | 24 | да | — | `62847ba24ed4ba22` |
| I-065 | `incident` | 23 | да | — | `6941f37401765b43` |
| I-065 | `incident-uq` | 24 | да | — | `62847ba24ed4ba22` |
| I-066 | `incident` | 23 | да | — | `cb346b78a4689c9a` |
| I-066 | `incident-uq` | 24 | да | — | `f685cc1b1457073d` |
| I-067 | `incident` | 23 | да | — | `9d0abce17241aba8` |
| I-067 | `incident-uq` | 24 | да | — | `62847ba24ed4ba22` |
| I-068 | `incident` | 23 | да | — | `66e454f9cc62f40f` |
| I-068 | `incident-uq` | 24 | да | — | `62847ba24ed4ba22` |
| I-069 | `incident` | 23 | да | — | `be767a4a9f86d374` |
| I-070 | `incident` | 23 | да | — | `00a0762212852e53` |
| I-071 | `incident` | 23 | да | — | `0f670db77fc42d3f` |
| I-072 | `incident` | 23 | да | — | `3f62b73f72466ce4` |
| I-072 | `incident-uq` | 24 | да | — | `8ad1d2b2c853fece` |
| I-073 | `incident` | 23 | да | — | `25e3e92c6890f93b` |
| I-074 | `incident` | 25 | да | — | `b8de59b5833613ca` |
| I-075 | `incident` | 25 | да | — | `c812901b9442d383` |
| I-076 | `incident` | 25 | да | 33, 35, 37, 87 | `9b51fa400e1b7901` |
| I-076 | `incident-uq` | 26 | да | 27, 29, 31, 38, 39, 42, 43, 47, 48, 49, 50, 70, 81, 87, 92, 94, 95, 98, 106, 110, 117, 119, 123, 134, 148, 154 | `032dd777366774b1` |
| I-077 | `incident` | 25 | да | — | `e9b4ba232f31155c` |
| I-078 | `incident` | 25 | да | 26 | `83647b261e9a1c60` |
| I-079 | `incident` | 25 | да | 23, 24 | `dfe62ef047e1cc64` |
| I-079 | `incident-uq` | 26 | да | 19, 27, 31, 33, 34, 35, 37, 38 | `07e38fa364505cb6` |
| I-080 | `incident` | 27 | да | — | `6b36ab13c44e4b0b` |
| I-080 | `incident-uq` | 34 | да | — | `35b82518aa22f0ff` |
| I-081 | `incident` | 27 | да | — | `54b71b77eba71596` |
| I-082 | `incident` | 27 | да | — | `f568bf7223173074` |
| I-082 | `incident-uq` | 28 | да | — | `10fdad791e9ed4b0` |
| I-083 | `incident` | 27 | да | — | `93abbd534d4c0ec2` |
| I-084 | `incident` | 27 | да | — | `9d5b3d286d2a4acd` |
| I-085 | `incident` | 27 | да | — | `e3ccb67d685d0d0b` |
| I-085 | `incident-uq` | 28 | да | — | `2be352429f6e74fe` |
| I-086 | `incident` | 27 | да | — | `1e66ad93b61bda9a` |
| I-086 | `incident-uq` | 32 | да | — | `873a3ed8cfefde2a` |
| I-087 | `incident` | 27 | да | 29 | `4d424b2864a2a36c` |
| I-088 | `incident` | 29 | да | — | `f65a2d4a01cc761f` |
| I-089 | `incident` | 29 | да | — | `d45e7fdf478410e2` |
| I-089 | `incident-uq` | 30 | да | — | `66bb99e2efdda1c3` |
| I-090 | `incident` | 29 | да | — | `04ccb904259ab558` |
| I-090 | `incident-uq` | 30 | да | — | `0b7b3775858a8869` |
| I-091 | `incident` | 29 | да | — | `c27aade962084788` |
| I-092 | `incident` | 29 | да | — | `470c4a9350a924c2` |
| I-093 | `incident` | 29 | да | — | `fa0fe451bb8f0330` |
| I-094 | `incident` | 29 | да | — | `27b6d02fdf23e80b` |
| I-095 | `incident` | 29 | да | — | `d533c18594fd2e77` |
| I-096 | `incident` | 29 | да | — | `b61c2a7df9e59764` |
| I-097 | `incident` | 29 | да | — | `4e1342035bd2fa83` |
| I-098 | `incident` | 29 | да | — | `60994c7cee5d5ea5` |
| I-099 | `incident` | 31 | да | — | `76d9c0b8a33a4cf3` |
| I-099 | `incident-uq` | 34 | да | — | `23f8012265070843` |
| I-100 | `incident` | 31 | да | — | `1ce30f243df135ec` |
| I-101 | `incident` | 31 | да | — | `9f7efbe9819342ec` |
| I-101 | `incident-uq` | 32 | да | — | `873a3ed8cfefde2a` |
| I-102 | `incident` | 31 | да | 27, 34 | `a72a2d637cc323a9` |
| I-102 | `incident-uq` | 34 | да | — | `a9f0b155f84d40be` |
| I-103 | `incident` | 31 | да | — | `f6350b165cafc939` |
| I-104 | `incident` | 31 | да | — | `0ffb58ade9f6ad91` |
| I-105 | `incident` | 31 | да | — | `73f94f8471112c56` |
| I-106 | `incident` | 33 | да | — | `a725c3afc2b9f02f` |
| I-107 | `incident` | 33 | да | — | `f412f20b40e289eb` |
| I-107 | `incident-uq` | 34 | да | — | `92d49c48140ee693` |
| I-108 | `incident` | 33 | да | — | `4be6ce26ea97a64e` |
| I-108 | `incident-uq` | 34 | да | — | `35b82518aa22f0ff` |
| I-109 | `incident` | 33 | да | 35 | `d98006b2bd2183b1` |
| I-110 | `incident` | 33 | да | 35, 37 | `1b3d264afef58dfa` |
| I-110 | `incident-uq` | 38 | да | — | `7f3a705e03ee001a` |
| I-111 | `incident` | 35 | да | — | `b98e26d3488bf843` |
| I-111 | `incident-uq` | 36 | да | — | `b38a7b01f2638f9d` |
| I-112 | `incident` | 35 | да | 36 | `f2aec3f97edb9982` |
| I-112 | `incident-uq` | 36 | да | — | `e47f5ee618593c65` |
| I-113 | `incident` | 35 | да | 33, 37 | `1b3d264afef58dfa` |
| I-113 | `incident-uq` | 38 | да | — | `7f3a705e03ee001a` |
| I-114 | `incident` | 35 | да | — | `6061e3f3a62f8167` |
| I-114 | `incident-uq` | 36 | да | — | `bad10a1f63137c2b` |
| I-115 | `incident` | 37 | да | 33, 35 | `1b3d264afef58dfa` |
| I-115 | `incident-uq` | 38 | да | — | `7f3a705e03ee001a` |
| I-116 | `incident` | 37 | да | — | `ec0178506c9eb08c` |
| I-116 | `incident-uq` | 38 | да | — | `de1f319f2532d3c4` |
| I-117 | `incident` | 37 | да | — | `aea4d6239ec2f576` |
| I-117 | `incident-uq` | 38 | да | — | `dae9ca6079376a61` |
| I-118 | `incident` | 39 | да | — | `0838e0a94d8d3e53` |
| I-118 | `incident-uq` | 54 | да | — | `a5face4e77ab651a` |
| I-119 | `incident` | 39 | да | — | `f313a22cd7b31bf5` |
| I-120 | `incident` | 39 | да | — | `bcebe1aefac425e5` |
| I-120 | `incident-uq` | 54 | да | — | `8c354a95de6c4a0b` |
| I-121 | `incident` | 39 | да | 51 | `e659d754045f12ce` |
| I-122 | `incident` | 39 | да | 51 | `ddc802b592fe8f1e` |
| I-123 | `incident` | 39 | да | 51 | `b099cc3b9beb0beb` |
| I-123 | `incident-uq` | 54 | да | — | `d462e1c9d8535026` |
| I-124 | `incident` | 39 | да | — | `1aa56c7574fc7145` |
| I-125 | `incident` | 41 | да | — | `d78522af1a809fa0` |
| I-126 | `incident` | 43 | да | — | `51c437cf3b656d3e` |
| I-127 | `incident` | 43 | да | — | `44b4ec8041f37970` |
| I-128 | `incident` | 43 | да | — | `2356b3c4c707ede4` |
| I-129 | `incident` | 43 | да | — | `c569f1ab560cbad7` |
| I-129 | `incident-uq` | 46 | да | — | `425b3515511c0c52` |
| I-130 | `incident` | 43 | да | — | `085c177032d6977e` |
| I-130 | `incident-uq` | 48 | да | 38, 42 | `5c6b24734e5df8c4` |
| I-131 | `incident` | 45 | да | — | `5fbd6b0366a3edd3` |
| I-132 | `incident` | 47 | да | — | `ea9e7c0f5d456049` |
| I-133 | `incident` | 47 | да | — | `2cf9506e7fa6bc4e` |
| I-133 | `incident-uq` | 48 | да | — | `02d5d4992c38ee13` |
| I-134 | `incident` | 47 | да | — | `f4e8281a22b7ff95` |
| I-135 | `incident` | 51 | да | — | `a9f62e6d4c72f9f0` |
| I-136 | `incident` | 51 | да | — | `908b78eb2b744c85` |
| I-136 | `incident-uq` | 54 | да | — | `c6703efd23ec2c79` |
| I-137 | `incident` | 51 | да | — | `f28b92ec05554a04` |
| I-137 | `incident-uq` | 54 | да | — | `eb7b21ba65e4605e` |
| I-138 | `incident` | 51 | да | 39 | `e659d754045f12ce` |
| I-139 | `incident` | 51 | да | 39 | `e57c3fe548b90d11` |
| I-139 | `incident-uq` | 54 | да | — | `5e8aa848aaaf73f6` |
| I-140 | `incident` | 51 | да | — | `fdd7d5cbce2a495b` |
| I-140 | `incident-uq` | 52 | да | — | `623056d34bc328d6` |
| I-141 | `incident` | 51 | да | 55, 65 | `c9ea0eca186fddad` |
| I-142 | `incident` | 53 | да | — | `d5519dc9013e824b` |
| I-143 | `incident` | 53 | да | — | `d6954685036c9809` |
| I-143 | `incident-uq` | 54 | да | — | `d462e1c9d8535026` |
| I-144 | `incident` | 53 | да | 55, 58, 59, 67, 70, 73, 87, 92, 94, 95, 98, 106, 110, 132, 134, 145, 148, 154 | `66015b6cfbe43e27` |
| I-144 | `incident-uq` | 58 | да | — | `8d238f9ac4bbb958` |
| I-145 | `incident` | 53 | да | — | `033e08e411118dad` |
| I-146 | `incident` | 55 | да | — | `10ac403a95a9c9b7` |
| I-147 | `incident` | 55 | да | 65 | `0d61dbb4609cb4f1` |
| I-148 | `incident` | 55 | да | — | `82f492e083d9e14e` |
| I-149 | `incident` | 55 | да | 59, 65, 67 | `df745d14daaf0180` |
| I-150 | `incident` | 55 | да | — | `8d6dda4b6b1b61d0` |
| I-151 | `incident` | 55 | да | 65 | `81b1b70b1c8a5129` |
| I-152 | `incident` | 55 | да | 65, 67, 73 | `14cb2e86bc6fea96` |
| I-153 | `incident` | 55 | да | 65 | `1e8bf807910a98ef` |
| I-154 | `incident` | 59 | да | — | `2d90988775d802a8` |
| I-155 | `incident` | 59 | да | — | `112ed68edf7fc587` |
| I-156 | `incident` | 59 | да | — | `7e7181ea936aecc0` |
| I-156 | `incident-rule` | 52 | да | — | `623056d34bc328d6` |
| I-157 | `incident` | 61 | да | — | `65b1ab8c052575b4` |
| I-158 | `incident` | 61 | да | — | `5c0910d9bbd0f6ac` |
| I-159 | `incident` | 61 | да | — | `6591372539880422` |
| I-159 | `incident-uq` | 62 | да | — | `15f1463b1c7e015f` |
| I-160 | `incident` | 61 | да | — | `af4983ad5617e6d7` |
| I-161 | `incident` | 63 | да | — | `0c3edebd26780ba4` |
| I-162 | `incident` | 63 | да | — | `8a7de403d13e5c21` |
| I-162 | `incident-rule` | 54 | да | — | `eb7b21ba65e4605e` |
| I-163 | `incident` | 63 | да | — | `386afd1efd5c6281` |
| I-164 | `incident` | 65 | да | — | `9c028c9e47749bef` |
| I-165 | `incident` | 65 | да | 66 | `4f621fffef5f8045` |
| I-165 | `incident-uq` | 66 | да | — | `aedb90c2d6c6f5b2` |
| I-166 | `incident` | 65 | да | — | `924907ac3a95a511` |
| I-166 | `incident-uq` | 66 | да | — | `aedb90c2d6c6f5b2` |
| I-167 | `incident` | 65 | да | — | `f5b5f2834c71e000` |
| I-167 | `incident-uq` | 66 | да | — | `e9af4825f43d46db` |
| I-168 | `incident` | 65 | да | 55, 59, 67 | `df745d14daaf0180` |
| I-169 | `incident` | 65 | да | 51, 55 | `70c041b763428c0e` |
| I-170 | `incident` | 65 | да | — | `1e05f2c76e9bfd57` |
| I-171 | `incident` | 65 | да | — | `2ae319c539fd265e` |
| I-172 | `incident` | 67 | да | 73, 91 | `5ce1bfc69781671d` |
| I-172 | `incident-uq` | 68 | да | — | `fcdec384c2155625` |
| I-173 | `incident` | 67 | да | — | `5e14e0573d30b8e0` |
| I-173 | `incident-uq` | 68 | да | — | `441a3b065354a708` |
| I-174 | `incident` | 67 | да | 39, 51, 73, 97 | `65dcf7319f74ea2b` |
| I-175 | `incident` | 67 | да | — | `8b178a15f6fbee3a` |
| I-176 | `incident` | 67 | да | — | `52e095a36943fcca` |
| I-177 | `incident` | 67 | да | — | `493b4b382b87b35c` |
| I-178 | `incident` | 67 | да | — | `ba3864abd359d086` |
| I-179 | `incident` | 69 | да | — | `aa4573214c9ea370` |
| I-180 | `incident` | 69 | да | — | `ef7381a45fcd8959` |
| I-181 | `incident` | 71 | да | — | `5f0057b652604cb3` |
| I-182 | `incident` | 71 | да | — | `cd003312d8e0995c` |
| I-183 | `incident` | 71 | да | — | `23a3708d5e8cfb47` |
| I-184 | `incident` | 71 | да | 72 | `a5ab483dd1f31cc9` |
| I-184 | `incident-uq` | 72 | да | — | `9d4f13583cadc162` |
| I-185 | `incident` | 71 | да | — | `51d8d66f6f8fbd34` |
| I-185 | `incident-uq` | 74 | да | — | `cafa9b1dcf607ed2` |
| I-186 | `incident` | 71 | да | — | `28c3b0d60552b203` |
| I-187 | `incident` | 71 | да | — | `720270b7f097447e` |
| I-188 | `incident` | 73 | да | — | `98061c85afff440c` |
| I-188 | `incident-uq` | 78 | да | — | `20b4e89c8c86493e` |
| I-189 | `incident` | 73 | да | — | `1bb5ac9cc2203ade` |
| I-190 | `incident` | 73 | да | — | `4a5ddfd02aaa2545` |
| I-191 | `incident` | 73 | да | 91 | `beeb4d941486c934` |
| I-192 | `incident` | 73 | да | — | `a4f605fde4c82f98` |
| I-193 | `incident` | 75 | да | 76 | `7f5d029659a05b73` |
| I-193 | `incident-uq` | 76 | да | — | `00fec1ed658ae472` |
| I-194 | `incident` | 75 | да | — | `6d67c19721f0553c` |
| I-195 | `incident` | 77 | да | — | `f8cac09a9721607c` |
| I-196 | `incident` | 77 | да | — | `23e59b878ba0f615` |
| I-197 | `incident` | 77 | да | — | `9f84dd8b9e969f38` |
| I-198 | `incident` | 77 | да | — | `b575a5f79162c2a5` |
| I-199 | `incident` | 79 | да | — | `cea3981658cd5afa` |
| I-200 | `incident` | 79 | да | — | `eadc8220383985bf` |
| I-201 | `incident` | 79 | да | — | `f8ea165d2d4d5ae1` |
| I-202 | `incident` | 81 | да | — | `03c9f98a28f63637` |
| I-203 | `incident` | 81 | да | — | `3937c6682eb0dcaf` |
| I-204 | `incident` | 81 | да | — | `9611b168c5133372` |
| I-205 | `incident` | 81 | да | — | `22c97c6f7830b0cc` |
| I-206 | `incident` | 83 | да | 121 | `aefca7448593780b` |
| I-207 | `incident` | 83 | да | — | `33442ee740164c46` |
| I-208 | `incident` | 83 | да | — | `25f50d3e1c6a98d2` |
| I-209 | `incident` | 85 | да | — | `600ae8ea61fea840` |
| I-209 | `incident-uq` | 86 | да | — | `7137462c62e65f4b` |
| I-210 | `incident` | 87 | да | — | `7b47263d5924ed66` |
| I-211 | `incident` | 87 | да | — | `ab8bd4639256b26b` |
| I-212 | `incident` | 87 | да | — | `00c949b0ff29ab1f` |
| I-213 | `incident` | 87 | да | 117, 119, 123 | `4d583ef920b49586` |
| I-214 | `incident` | 87 | да | — | `4cf29d137ece5f45` |
| I-215 | `incident` | 87 | да | — | `bfe8bb426a6cded2` |
| I-216 | `incident` | 87 | да | — | `d2283768903ddcb3` |
| I-217 | `incident` | 91 | да | — | `599ebd4b7c7b8f20` |
| I-217 | `incident-uq` | 92 | да | — | `249408af9f421b9f` |
| I-218 | `incident` | 91 | да | — | `4188fc557be951d3` |
| I-219 | `incident` | 91 | да | 73 | `1a028b5b4c0436ce` |
| I-220 | `incident` | 91 | да | — | `88637a95af04c5f5` |
| I-221 | `incident` | 93 | да | — | `006be40c23f6bdc0` |
| I-222 | `incident` | 93 | да | — | `c06ea59957e56e8c` |
| I-222 | `incident-uq` | 94 | да | — | `6183410e99fbd0b1` |
| I-223 | `incident` | 93 | да | — | `6a0b78756ff385c8` |
| I-224 | `incident` | 93 | да | — | `22816f8c944d7406` |
| I-225 | `incident` | 93 | да | — | `0464f753dbbb058e` |
| I-226 | `incident` | 95 | да | — | `5edb8b2079912bbc` |
| I-227 | `incident` | 95 | да | — | `eb1dbbc99d519c0c` |
| I-228 | `incident` | 95 | да | — | `82485517d9011d5f` |
| I-229 | `incident` | 95 | да | — | `5d201c455559958a` |
| I-230 | `incident` | 97 | да | — | `fc8c8a00a429d27a` |
| I-230 | `incident-uq` | 98 | да | 94, 95 | `e6476e5426d2f00a` |
| I-231 | `incident` | 97 | да | 55 | `5253815f4b71a342` |
| I-231 | `incident-uq` | 98 | да | 70, 92, 94, 106, 110, 132, 134, 148, 154 | `2c85d4b55523622b` |
| I-232 | `incident` | 97 | да | — | `d26032cc7ee16b85` |
| I-233 | `incident` | 97 | да | — | `a5c73731ae813adf` |
| I-234 | `incident` | 99 | да | — | `2f54fd9e96ce2409` |
| I-235 | `incident` | 99 | да | — | `7c620cfcd35f7a64` |
| I-235 | `incident-uq` | 100 | да | — | `d35549a492f3371b` |
| I-236 | `incident` | 99 | да | — | `48615e344386c9e8` |
| I-236 | `incident-uq` | 100 | да | — | `97c726a88455da9e` |
| I-237 | `incident` | 101 | да | — | `ca65154f1e086fe7` |
| I-238 | `incident` | 101 | да | — | `d59fdf9415d4868a` |
| I-239 | `incident` | 101 | да | — | `c243a9df610605c2` |
| I-239 | `incident-uq` | 104 | да | — | `53fecf39f4832adf` |
| I-240 | `incident` | 101 | да | — | `21aaff904835cc81` |
| I-240 | `incident-uq` | 102 | да | — | `8ce06cef2a8e996b` |
| I-241 | `incident` | 101 | да | — | `fb4be11d9fc039c0` |
| I-242 | `incident` | 103 | да | — | `8572a88760695c2b` |
| I-242 | `incident-uq` | 104 | да | — | `00794cc95973d0a6` |
| I-243 | `incident` | 103 | да | — | `e185d72f9626dbf8` |
| I-244 | `incident` | 107 | да | — | `847b6a2c206ee0ce` |
| I-244 | `incident-uq` | 108 | да | — | `cbe507d037d384df` |
| I-245 | `incident` | 107 | да | — | `70c746384c71bd8e` |
| I-245 | `incident-uq` | 108 | да | — | `cbe507d037d384df` |
| I-246 | `incident` | 107 | да | — | `1836dbb2055f6cd4` |
| I-247 | `incident` | 107 | да | — | `d9c74a28282e0561` |
| I-248 | `incident` | 109 | да | — | `d7c10cf975657902` |
| I-249 | `incident` | 109 | да | — | `546e7bd37a9453f7` |
| I-250 | `incident` | 109 | да | — | `0ae3d2ff3cc56094` |
| I-251 | `incident` | 111 | да | — | `30d4adb23dcafa92` |
| I-252 | `incident` | 111 | да | — | `45ce66a21f0b2510` |
| I-253 | `incident` | 111 | да | — | `1d149908a8bff4bb` |
| I-254 | `incident` | 111 | да | — | `29371579d37609ea` |
| I-255 | `incident` | 111 | да | — | `6728f4290d152f0e` |
| I-256 | `incident` | 111 | да | — | `2c44d3182d1aba9f` |
| I-256 | `incident-uq` | 112 | да | — | `6c35b3e2817e4093` |
| I-257 | `incident` | 113 | да | — | `c2e23095265ac2fe` |
| I-257 | `incident-uq` | 116 | да | — | `e53c4c7cc28fcc58` |
| I-258 | `incident` | 113 | да | — | `baedb3c8c6fb9b72` |
| I-259 | `incident` | 113 | да | 134, 148, 154 | `4ebb43904901ad79` |
| I-260 | `incident` | 113 | да | — | `d2b67afa41047241` |
| I-261 | `incident` | 113 | да | — | `2a00b32d38d7d1f8` |
| I-262 | `incident` | 115 | да | — | `0621bad9389f98d5` |
| I-263 | `incident` | 117 | да | 119, 121, 123 | `0659364e600e8852` |
| I-264 | `incident` | 117 | да | 119, 121, 123 | `fedb716080682e60` |
| I-264 | `incident-rule` | 116 | да | — | `97869549d447d182` |
| I-265 | `incident` | 117 | да | 119, 121, 123 | `92ad8feb5adcf257` |
| I-265 | `incident-rule` | 116 | да | — | `f9e3f5ba6c68e7e9` |
| I-266 | `incident` | 117 | да | 87, 119, 123 | `c9ab2d8413c3ba24` |
| I-266 | `incident-rule` | 116 | да | — | `f9e3f5ba6c68e7e9` |
| I-267 | `incident` | 117 | да | 119, 123 | `53727e1bab247c0a` |
| I-267 | `incident-uq` | 118 | да | — | `1695f1a8ac39a0ed` |
| I-268 | `incident` | 117 | да | 87, 119, 123 | `cb0ebddc03a9850f` |
| I-268 | `incident-uq` | 118 | да | — | `6d4b303dd118209e` |
| I-269 | `incident` | 117 | да | — | `3c20868cd8d33825` |
| I-270 | `incident` | 119 | да | 123 | `e19023964eb081dc` |
| I-270 | `incident-uq` | 120 | да | — | `54528986962cb40e` |
| I-271 | `incident` | 119 | да | — | `75af94e4f47bde01` |
| I-272 | `incident` | 119 | да | 123 | `a05029cca76e44f8` |
| I-273 | `incident` | 121 | да | — | `5fd43a937f12d3fc` |
| I-274 | `incident` | 121 | да | — | `29b18ba33347aa21` |
| I-275 | `incident` | 123 | да | — | `61089f3923d11ac1` |
| I-275 | `incident-rule` | 118 | да | — | `9a24baa9b7c6069d` |
| I-276 | `incident` | 123 | да | 81, 87, 117, 119 | `984d40e980e04016` |
| I-277 | `incident` | 123 | да | 119 | `00fb39aaf1c1b7db` |
| I-277 | `incident-rule` | 120 | да | — | `54528986962cb40e` |
| I-278 | `incident` | 123 | да | 117, 119, 121 | `0659364e600e8852` |
| I-279 | `incident` | 123 | да | 117, 119, 121 | `5c080b29f00b63fc` |
| I-279 | `incident-rule` | 116 | да | — | `f9e3f5ba6c68e7e9` |
| I-280 | `incident` | 123 | да | — | `1b2eb9ea7eb2c5c6` |
| I-281 | `incident` | 125 | да | — | `c54f734bd5eefd44` |
| I-281 | `incident-uq` | 126 | да | — | `85993e07d169302c` |
| I-282 | `incident` | 125 | да | — | `ed07fbbd0cf95c91` |
| I-282 | `incident-uq` | 128 | да | — | `3d8825c1397f8608` |
| I-283 | `incident` | 125 | да | — | `5e3a63c1fe7cbaf6` |
| I-283 | `incident-uq` | 130 | да | — | `57d96ed936cd6d78` |
| I-284 | `incident` | 125 | да | — | `c2e50be691cb863e` |
| I-285 | `incident` | 125 | да | — | `0ee933f9e6922ed3` |
| I-286 | `incident` | 125 | да | — | `154593767b4c38f0` |
| I-287 | `incident` | 125 | да | — | `47a8c62b17e6478f` |
| I-288 | `incident` | 127 | да | — | `e5d0d5c6f7c136d3` |
| I-288 | `incident-uq` | 130 | да | — | `c338e57e63d39580` |
| I-289 | `incident` | 127 | да | — | `070ab20d07c9fa43` |
| I-290 | `incident` | 129 | да | — | `c3e0e88a956d4ba4` |
| I-291 | `incident` | 129 | да | — | `8db80d19f1e8fa4a` |
| I-291 | `incident-uq` | 130 | да | — | `c338e57e63d39580` |
| I-292 | `incident` | 129 | да | — | `e03308e07aeafbf8` |
| I-293 | `incident` | 131 | да | — | `d754ee7ccdcf81fc` |
| I-294 | `incident` | 131 | да | — | `33667ea00b4e58f9` |
| I-295 | `incident` | 131 | да | — | `4777b0ad8780d964` |
| I-296 | `incident` | 131 | да | — | `eaf41340ae47a6b2` |
| I-297 | `incident` | 131 | да | 70, 92, 94, 95, 98, 106, 110, 132, 134, 145, 148 | `d9c5b23060e1cd69` |
| I-298 | `incident` | 133 | да | — | `79df985d11631b32` |
| I-299 | `incident` | 133 | да | — | `0af6bb9ef55940a5` |
| I-300 | `incident` | 133 | да | — | `994fa1bb2f3dfb10` |
| I-301 | `incident` | 135 | да | — | `27b4bccaca727a56` |
| I-302 | `incident` | 135 | да | — | `9e6db5df00dc49e6` |
| I-303 | `incident` | 137 | да | — | `6967b0fe67aef0a7` |
| I-304 | `incident` | 137 | да | — | `dae21d05659f591d` |
| I-305 | `incident` | 137 | да | — | `640e1cfc22c526f7` |
| I-305 | `incident-uq` | 144 | да | — | `b6700c388ca19cdc` |
| I-306 | `incident` | 139 | да | — | `4bf22141819c4c3b` |
| I-307 | `incident` | 139 | да | 140 | `92a8b2b3ebf0412c` |
| I-307 | `incident-uq` | 140 | да | — | `e318515892eeb49b` |
| I-308 | `incident` | 139 | да | — | `e2cfd7777203f201` |
| I-309 | `incident` | 141 | да | — | `fd8842e2aeda35c1` |
| I-309 | `incident-uq` | 144 | да | — | `b6700c388ca19cdc` |
| I-310 | `incident` | 141 | да | — | `6023a4fa380c0f0e` |
| I-311 | `incident` | 143 | да | — | `f73f252ab34db9dd` |
| I-311 | `incident-uq` | 144 | да | — | `b6700c388ca19cdc` |
| I-312 | `incident` | 143 | да | — | `bc4c4e44895965aa` |
| I-313 | `incident` | 143 | да | — | `0d4b80a6cb924090` |
| I-314 | `incident` | 145 | да | — | `66b85f6da555501c` |
| I-315 | `incident` | 145 | да | — | `3e9d96402451a34a` |
| I-316 | `incident` | 145 | да | — | `cb210c42f387e54e` |
| I-316 | `incident-uq` | 148 | да | — | `d6fcf4311b8a58af` |
| I-317 | `incident` | 145 | да | — | `c87d6672d780a35b` |
| I-318 | `incident` | 145 | да | — | `f03af1ea65449331` |
| I-318 | `incident-uq` | 146 | да | — | `ea291682e0df11a7` |
| I-319 | `incident` | 145 | да | — | `d139e38949157317` |
| I-320 | `incident` | 147 | да | — | `736f093aa481eb76` |
| I-321 | `incident` | 149 | да | 150 | `35f324aa61c91bcf` |
| I-321 | `incident-uq` | 150 | да | — | `40bb75eb9ed75ec6` |
| I-322 | `incident` | 149 | да | — | `39e04302f9156569` |
| I-323 | `incident` | 151 | да | — | `50f8d91c59a104c7` |
| I-324 | `incident` | 151 | да | — | `8b23a85ee868d338` |
| I-324 | `incident-uq` | 152 | да | — | `59c54f206c1b817e` |
| I-325 | `incident` | 151 | да | — | `7bc720d359c37a7f` |
| I-326 | `incident` | 151 | да | — | `d61ae2f8df335cb2` |
| I-327 | `incident` | 151 | да | — | `ca6c9aefd418f63d` |
| I-328 | `incident` | 153 | да | — | `b8b210f025dc6ff1` |
| I-329 | `incident` | 153 | да | — | `ef8b42e4e514619c` |
| I-330 | `incident` | 155 | да | — | `8362ef7baca487d9` |
| I-331 | `incident` | 155 | да | — | `6e3d58f0bdda7868` |
| I-332 | `incident` | 155 | да | — | `9e27a0f5f80cc498` |
| I-333 | `incident` | 155 | да | — | `d85424c51989cde9` |
| N-01 | `negative` | 1 | да | — | `b99b783263fe5a9d` |
| N-02 | `negative` | 3 | да | — | `b694506fee73ee86` |
| N-02 | `negative-uq` | 4 | да | — | `9769394db1295b0c` |
| N-03 | `negative` | 5 | да | — | `c2e4891df9529c87` |
| N-04 | `negative` | 9 | да | — | `c8e87df58ce7d824` |
| N-04 | `negative-uq` | 10 | да | — | `65f85ee8601c6707` |
| N-05 | `negative` | 13 | да | — | `c0deea04dc479ac2` |
| N-05 | `negative-uq` | 14 | да | 70, 92, 94, 98, 106, 110, 134, 148, 154 | `5a0e672cf737df2e` |
| N-06 | `negative` | 21 | да | — | `092f472cd97743c2` |
| N-07 | `negative` | 25 | да | — | `f6b6a82a4f58f147` |
| N-08 | `negative` | 37 | да | — | `f7ccc27a84b0b4d7` |
| N-08 | `negative-uq` | 36 | да | — | `89eb79f9ac2b3874` |
| N-09 | `negative` | 39 | да | — | `7424e10d1aeceadf` |
| N-10 | `negative` | 43 | да | — | `faf4a9206e3301af` |
| N-11 | `negative` | 49 | да | — | `f2c9b9478a8a1904` |
| N-12 | `negative` | 59 | да | — | `84083d69bc70fca3` |
| N-13 | `negative` | 69 | да | — | `8de459f2dde7613d` |
| N-13 | `negative-uq` | 68 | да | — | `76fe979871c71030` |
| N-14 | `negative` | 75 | да | — | `c8513747a18209dd` |
| N-15 | `negative` | 89 | да | — | `20879fb84f671107` |
| N-15 | `negative-uq` | 88 | да | — | `b50ce552b016176c` |
| N-16 | `negative` | 93 | да | — | `03b9b719d1e85047` |
| N-17 | `negative` | 95 | да | — | `358e66efbaf33714` |
| N-18 | `negative` | 105 | да | — | `6c6cc7b29505cfa0` |
| N-18 | `negative-uq` | 104 | да | — | `53fecf39f4832adf` |
| N-19 | `negative` | 109 | да | — | `794b0ed3c4247d8d` |
| N-19 | `negative-uq` | 108 | да | — | `cbe507d037d384df` |
| N-20 | `negative` | 125 | да | — | `ceae553b48f5a959` |
| N-21 | `negative` | 123 | да | — | `9713bdd282d8125e` |
| N-21 | `negative-uq` | 122 | да | — | `f4c8f044aa1aaa2f` |
| N-22 | `negative` | 103 | да | — | `6005d6da0d027db4` |
| N-22 | `negative-uq` | 102 | да | — | `3f19540e856cee61` |
| N-23 | `negative` | 127 | да | — | `6ae27eec599a5ee3` |
| N-24 | `negative` | 133 | да | — | `d27d10c0c66cf80c` |
| N-25 | `negative` | 149 | да | — | `90aadc868d883536` |
| N-26 | `negative` | 149 | да | — | `a78643a7bf577d0b` |
| N-27 | `negative` | 149 | да | — | `aaf80b618dafb112` |
| N-27 | `negative-uq` | 148 | да | — | `d6fcf4311b8a58af` |
| SC-01 | `success` | 8 | да | — | `af9eba0117f2ec7d` |
| SC-02 | `success` | 10 | да | — | `a3757aa3e542fa19` |
| SC-03 | `success` | 10 | да | — | `45849e0df7c4eaff` |
| SC-04 | `success` | 10 | да | — | `ef0a1712ad973521` |
| SC-05 | `success` | 10 | да | — | `b329fcfd1d1ac284` |
| SC-06 | `success` | 10 | да | — | `6affb9ea51a89084` |
| SC-07 | `success` | 12 | да | — | `83660adf0122b400` |
| SC-08 | `success` | 12 | да | — | `fb7c23708c52dffe` |
| SC-09 | `success` | 12 | да | — | `173f7163c979ee48` |
| SC-10 | `success` | 12 | да | — | `91f256daadfdd76b` |
| SC-11 | `success` | 14 | да | 70, 92, 94, 98, 106, 110, 134, 148, 154 | `e5fad3357eb8363b` |
| SC-12 | `success` | 16 | да | — | `4431f4a44db4b55c` |
| SC-13 | `success` | 16 | да | — | `88c706710c919ba8` |
| SC-14 | `success` | 20 | да | — | `41608d6028295e12` |
| SC-15 | `success` | 22 | да | — | `eefe2a2b83c87ac3` |
| SC-16 | `success` | 24 | да | — | `8feec78bf17723ec` |
| SC-17 | `success` | 28 | да | — | `dfa7d9de0e1b8414` |
| SC-18 | `success` | 30 | да | — | `3c648559b3355b01` |
| SC-19 | `success` | 32 | да | — | `873a3ed8cfefde2a` |
| SC-20 | `success` | 34 | да | — | `92d49c48140ee693` |
| SC-21 | `success` | 36 | да | — | `de8946948840f01f` |
| SC-22 | `success` | 36 | да | — | `e47f5ee618593c65` |
| SC-23 | `success` | 38 | да | — | `7f3a705e03ee001a` |
| SC-24 | `success` | 38 | да | — | `de1f319f2532d3c4` |
| SC-25 | `success` | 46 | да | — | `50bbdbd3637079c5` |
| SC-26 | `success` | 52 | да | — | `e06e9457407ba808` |
| SC-27 | `success` | 54 | да | — | `395eef8ea34b56be` |
| SC-28 | `success` | 54 | да | — | `8c354a95de6c4a0b` |
| SC-29 | `success` | 54 | да | — | `5e8aa848aaaf73f6` |
| SC-30 | `success` | 58 | да | — | `8d238f9ac4bbb958` |
| SC-31 | `success` | 66 | да | — | `29b65c50f7d89d7e` |
| SC-32 | `success` | 66 | да | — | `97c8ca00ef1be987` |
| SC-33 | `success` | 68 | да | — | `a145ad290d9b27a8` |
| SC-34 | `success` | 68 | да | — | `e23bdbeb1715d41c` |
| SC-35 | `success` | 70 | да | — | `b3e6862b5c21d556` |
| SC-36 | `success` | 72 | да | — | `9d4f13583cadc162` |
| SC-37 | `success` | 74 | да | — | `cafa9b1dcf607ed2` |
| SC-38 | `success` | 76 | да | — | `00fec1ed658ae472` |
| SC-39 | `success` | 88 | да | — | `b50ce552b016176c` |
| SC-40 | `success` | 90 | да | — | `4c218a779f5da727` |
| SC-41 | `success` | 92 | да | — | `249408af9f421b9f` |
| SC-42 | `success` | 94 | да | — | `8c2c08dce52b6880` |
| SC-43 | `success` | 102 | да | — | `3f19540e856cee61` |
| SC-44 | `success` | 104 | да | — | `53fecf39f4832adf` |
| SC-45 | `success` | 104 | да | — | `00794cc95973d0a6` |
| SC-46 | `success` | 108 | да | — | `cbe507d037d384df` |
| SC-47 | `success` | 116 | да | — | `7c99ec14b339adda` |
| SC-48 | `success` | 116 | да | — | `e53c4c7cc28fcc58` |
| SC-49 | `success` | 116 | да | — | `e51344ab90e206be` |
| SC-50 | `success` | 116 | да | — | `83fac94aabe3099a` |
| SC-51 | `success` | 116 | да | — | `97869549d447d182` |
| SC-52 | `success` | 118 | да | — | `6d4b303dd118209e` |
| SC-53 | `success` | 118 | да | — | `9a24baa9b7c6069d` |
| SC-54 | `success` | 122 | да | — | `49e87e9c25247c14` |
| SC-55 | `success` | 124 | да | — | `97d68c3a7e0f6289` |
| SC-56 | `success` | 124 | да | — | `97c3d29bad19bf59` |
| SC-57 | `success` | 126 | да | — | `f23ebab277c8e5d6` |
| SC-58 | `success` | 128 | да | — | `3d8825c1397f8608` |
| SC-59 | `success` | 130 | да | — | `405174774f0f6be4` |
| SC-60 | `success` | 130 | да | — | `86747e259542a55c` |
| SC-61 | `success` | 142 | да | — | `66f8c717b5a2467b` |
| SC-62 | `success` | 144 | да | — | `675e076fb3032141` |
| SC-63 | `success` | 148 | да | — | `31b14d4cbd7cf720` |
| SC-64 | `success` | 150 | да | — | `40bb75eb9ed75ec6` |
| SC-65 | `success` | 152 | да | — | `d7d05f7ede921c32` |
