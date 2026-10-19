---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/373"
related_artifacts:
  - "experiments/issue_373_verify_quotes.py"
---

# Журнал сверки цитат прогона RUN-0073

> Файл **порождён** скриптом [`experiments/issue_373_golden_set.py`](../../../../experiments/issue_373_golden_set.py) из вывода [`experiments/issue_373_verify_quotes.py`](../../../../experiments/issue_373_verify_quotes.py) — не редактируйте вручную.

Каждая цитата разметки искалась в тексте заявленной реплики экспорта после нормализации (пробелы схлопнуты, `*` и `` ` `` удалены). Текст экспорта в журнал не копируется: фиксируется SHA-256 нормализованной цитаты.

- SHA-256 экспорта: `318212fec8f2c3c4078bea71d32bb4607d74766961e64722e3c82cf875b01c27`
- Реплик в ветке: 106
- Цитат проверено: 279; не найдено в заявленной реплике: **0**
- Встречаются ещё и в других репликах: 74 (заявленная реплика входит в список найденных — привязка однозначна по номеру реплики)

| Вид цитаты | Проверено |
| --- | --- |
| `incident` | 149 |
| `incident-uq` | 92 |
| `negative` | 12 |
| `negative-uq` | 4 |
| `success` | 22 |

| Ссылка | Вид | Реплика | Найдена | Также в репликах | SHA-256 (нормализованной) |
| --- | --- | --- | --- | --- | --- |
| I-001 | `incident` | 0 | да | — | `28d45e61e7f74bfa` |
| I-001 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-002 | `incident` | 0 | да | — | `a2a23d6cb84ee943` |
| I-002 | `incident-uq` | 60 | да | — | `5eac20ddd807a3fc` |
| I-003 | `incident` | 0 | да | — | `eeeabd4efab4fadd` |
| I-003 | `incident-uq` | 60 | да | — | `5eac20ddd807a3fc` |
| I-004 | `incident` | 0 | да | — | `eac064c2cefc3490` |
| I-004 | `incident-uq` | 60 | да | — | `5eac20ddd807a3fc` |
| I-005 | `incident` | 0 | да | — | `c438f1c62db11b15` |
| I-005 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-006 | `incident` | 0 | да | — | `b818e5370b7fc280` |
| I-006 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-007 | `incident` | 0 | да | — | `54ba88a11b6a5a5c` |
| I-007 | `incident-uq` | 74 | да | — | `f61b26ad799c74f8` |
| I-008 | `incident` | 0 | да | 5 | `3a8faaf6ef3791cd` |
| I-008 | `incident-uq` | 16 | да | — | `c144cbd027d34b62` |
| I-009 | `incident` | 0 | да | — | `915185e4fdab916b` |
| I-009 | `incident-uq` | 16 | да | — | `c144cbd027d34b62` |
| I-010 | `incident` | 0 | да | 11, 69, 71 | `21335df7ced5c909` |
| I-010 | `incident-uq` | 78 | да | — | `d0f11ddf4a2ee136` |
| I-011 | `incident` | 0 | да | — | `a88cd1ec16e08683` |
| I-012 | `incident` | 0 | да | — | `4889a9ce32b2e6df` |
| I-013 | `incident` | 0 | да | — | `b6dc0bfce53190de` |
| I-014 | `incident` | 0 | да | — | `75af94e4f47bde01` |
| I-014 | `incident-uq` | 66 | да | — | `a1f2e7efec2d3b5c` |
| I-015 | `incident` | 0 | да | — | `9eef370d5369795c` |
| I-016 | `incident` | 0 | да | — | `e09eda060a7403fb` |
| I-017 | `incident` | 0 | да | 25 | `fb4c6366c103980c` |
| I-017 | `incident-uq` | 8 | да | — | `79512c702c890af7` |
| I-018 | `incident` | 0 | да | — | `f3746c44b96fac16` |
| I-018 | `incident-uq` | 66 | да | — | `a1f2e7efec2d3b5c` |
| I-019 | `incident` | 5 | да | — | `5bb94cf2f111f47c` |
| I-019 | `incident-uq` | 60 | да | — | `5eac20ddd807a3fc` |
| I-020 | `incident` | 7 | да | 8 | `0428b454bd89d1ef` |
| I-020 | `incident-uq` | 8 | да | — | `fcd46653951bef2f` |
| I-021 | `incident` | 7 | да | — | `20f8a5bbcd06cef2` |
| I-021 | `incident-uq` | 8 | да | — | `90e5a2e2354ec33f` |
| I-022 | `incident` | 7 | да | — | `c52a835ae0e2ff27` |
| I-022 | `incident-uq` | 8 | да | — | `9fdfa3753cb1824b` |
| I-023 | `incident` | 7 | да | — | `24a3ecce42cd74b2` |
| I-024 | `incident` | 7 | да | — | `24b892ea3fa588cd` |
| I-025 | `incident` | 7 | да | — | `31cb2ec4928d9aa7` |
| I-026 | `incident` | 9 | да | — | `89d70a4b6f42e86e` |
| I-026 | `incident-uq` | 10 | да | — | `29413050209978eb` |
| I-027 | `incident` | 11 | да | 14 | `808ff520a990db96` |
| I-027 | `incident-uq` | 14 | да | — | `2d8d030bab9b817c` |
| I-028 | `incident` | 11 | да | — | `b0b53b1eb1b759e7` |
| I-028 | `incident-uq` | 14 | да | — | `2d8d030bab9b817c` |
| I-029 | `incident` | 11 | да | — | `a8e23009ca013165` |
| I-029 | `incident-uq` | 16 | да | — | `7e40e3e5f3bc6541` |
| I-030 | `incident` | 11 | да | 16 | `ceb0b73ec3f4f12c` |
| I-030 | `incident-uq` | 16 | да | — | `65499c2ba84c33f4` |
| I-031 | `incident` | 11 | да | 16 | `caf6daa41ac0aff3` |
| I-031 | `incident-uq` | 16 | да | — | `bba92de05882cfe2` |
| I-032 | `incident` | 11 | да | 0, 25, 29, 35, 37, 43, 45, 47, 104 | `feda6a02862e5eef` |
| I-032 | `incident-uq` | 16 | да | — | `c69c483ca44c5fe2` |
| I-033 | `incident` | 11 | да | 16 | `a79d729187587237` |
| I-033 | `incident-uq` | 16 | да | — | `c144cbd027d34b62` |
| I-034 | `incident` | 11 | да | — | `56ebdcc49368d208` |
| I-034 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-035 | `incident` | 11 | да | 0, 69, 71 | `21335df7ced5c909` |
| I-035 | `incident-uq` | 78 | да | — | `d0f11ddf4a2ee136` |
| I-036 | `incident` | 11 | да | — | `9c316175edb49c57` |
| I-037 | `incident` | 15 | да | — | `334184c713dd1ef6` |
| I-038 | `incident` | 19 | да | — | `7eb9e865dbdb16f5` |
| I-038 | `incident-uq` | 20 | да | — | `04b4bc50050ad77b` |
| I-039 | `incident` | 19 | да | — | `fba2679e83cb43b7` |
| I-039 | `incident-uq` | 22 | да | 19, 24, 104 | `e078b8ed475cbe81` |
| I-040 | `incident` | 23 | да | — | `b58167a8fced5a54` |
| I-041 | `incident` | 23 | да | — | `0b45a21fa02dda67` |
| I-042 | `incident` | 25 | да | — | `2cb1977e025a37e9` |
| I-042 | `incident-uq` | 26 | да | — | `05bfbdb20c8647f1` |
| I-043 | `incident` | 25 | да | 29, 32 | `44cd86d8727b22f0` |
| I-043 | `incident-uq` | 32 | да | — | `162eddb9d390ec49` |
| I-044 | `incident` | 25 | да | 0 | `fce10f0bc6219b73` |
| I-044 | `incident-uq` | 60 | да | — | `5eac20ddd807a3fc` |
| I-045 | `incident` | 25 | да | 69 | `90a55a1c1bd95d81` |
| I-046 | `incident` | 25 | да | 0 | `3bfe0874b7b28b8e` |
| I-046 | `incident-uq` | 60 | да | — | `5eac20ddd807a3fc` |
| I-047 | `incident` | 25 | да | — | `2a00bfba4c2cd679` |
| I-048 | `incident` | 25 | да | — | `79a2cfde287ead53` |
| I-048 | `incident-uq` | 26 | да | — | `de9ac773c3a9e07a` |
| I-049 | `incident` | 25 | да | 69, 73, 75 | `9ab8f27b42dba7b6` |
| I-049 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-050 | `incident` | 27 | да | — | `24dc1da813fca8e5` |
| I-051 | `incident` | 29 | да | 25 | `e922e69b14dfa176` |
| I-051 | `incident-uq` | 32 | да | — | `e6bbb94ebb7c948f` |
| I-052 | `incident` | 29 | да | 25, 32, 41 | `bdeb6759635ef799` |
| I-052 | `incident-uq` | 32 | да | — | `162eddb9d390ec49` |
| I-053 | `incident` | 29 | да | 25, 35, 37, 43 | `4c6bd701b9f5b5ab` |
| I-053 | `incident-uq` | 44 | да | — | `231a0996c12a73fb` |
| I-054 | `incident` | 31 | да | — | `481428e909667571` |
| I-054 | `incident-uq` | 36 | да | — | `a6255f97081a56f6` |
| I-055 | `incident` | 33 | да | — | `a0581192e4461db5` |
| I-056 | `incident` | 35 | да | 37, 46, 47, 54, 104 | `93cef5a826961db6` |
| I-056 | `incident-uq` | 36 | да | — | `a6255f97081a56f6` |
| I-057 | `incident` | 43 | да | — | `92325fc529da8959` |
| I-058 | `incident` | 43 | да | — | `e698404f48ce9a5d` |
| I-058 | `incident-uq` | 46 | да | — | `47d3cdc6410a2731` |
| I-059 | `incident` | 43 | да | 45, 46 | `14562640d1810da8` |
| I-059 | `incident-uq` | 46 | да | — | `47d3cdc6410a2731` |
| I-060 | `incident` | 43 | да | 25, 29, 35, 37 | `4c6bd701b9f5b5ab` |
| I-060 | `incident-uq` | 44 | да | — | `231a0996c12a73fb` |
| I-061 | `incident` | 45 | да | — | `e037cef3b57878aa` |
| I-062 | `incident` | 47 | да | 25, 29, 37, 43, 45, 50, 51 | `d36950def6124679` |
| I-062 | `incident-uq` | 50 | да | 51 | `c0596e4014a96f35` |
| I-063 | `incident` | 49 | да | — | `cd30cd591d51cbec` |
| I-063 | `incident-uq` | 50 | да | 51 | `b855a8ddc362fde8` |
| I-064 | `incident` | 51 | да | — | `e2f19e07ab317ab1` |
| I-065 | `incident` | 51 | да | — | `2da2de63813b55a4` |
| I-066 | `incident` | 51 | да | — | `425a87bb9e1e57d8` |
| I-067 | `incident` | 53 | да | — | `de5e5018bce59dc5` |
| I-067 | `incident-uq` | 78 | да | — | `a3c9608e59c263d5` |
| I-068 | `incident` | 53 | да | — | `3c6a0379ab81ec8d` |
| I-069 | `incident` | 55 | да | — | `eff675739bad02e7` |
| I-070 | `incident` | 57 | да | 60, 61, 63, 67, 69, 73 | `9d1d72c99a727100` |
| I-070 | `incident-uq` | 74 | да | — | `f61b26ad799c74f8` |
| I-071 | `incident` | 57 | да | 60 | `f86114599a69268d` |
| I-071 | `incident-uq` | 60 | да | — | `5eac20ddd807a3fc` |
| I-072 | `incident` | 57 | да | 60, 61 | `151ea64fd0a5bb78` |
| I-072 | `incident-uq` | 62 | да | — | `c430467361f4c5db` |
| I-073 | `incident` | 59 | да | — | `4c17ea6d80949877` |
| I-074 | `incident` | 61 | да | — | `33871ffea4da6d3f` |
| I-074 | `incident-uq` | 74 | да | — | `f61b26ad799c74f8` |
| I-075 | `incident` | 65 | да | — | `da3e3733a5266d08` |
| I-075 | `incident-uq` | 66 | да | — | `a1f2e7efec2d3b5c` |
| I-076 | `incident` | 65 | да | 66 | `395a093eda2ee29e` |
| I-076 | `incident-uq` | 66 | да | — | `a1f2e7efec2d3b5c` |
| I-077 | `incident` | 69 | да | — | `563af2648401e16e` |
| I-077 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-078 | `incident` | 69 | да | 73, 75 | `87d6cfa66b9fae4b` |
| I-078 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-079 | `incident` | 69 | да | 57, 60, 61, 63, 67, 73 | `9d1d72c99a727100` |
| I-079 | `incident-uq` | 74 | да | — | `f61b26ad799c74f8` |
| I-080 | `incident` | 69 | да | 51, 71 | `aae34a53bea47746` |
| I-080 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-081 | `incident` | 69 | да | 71, 73, 75 | `54e624dd30f35a51` |
| I-081 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-082 | `incident` | 69 | да | 23, 25 | `62c101d40a7c28c2` |
| I-083 | `incident` | 69 | да | 0, 5, 11, 25, 31, 61, 71, 85 | `e545a5af59c65dba` |
| I-083 | `incident-uq` | 78 | да | — | `d0f11ddf4a2ee136` |
| I-084 | `incident` | 69 | да | — | `720fbf91b8ab0128` |
| I-084 | `incident-uq` | 70 | да | — | `630c11117a8f8fd5` |
| I-085 | `incident` | 69 | да | — | `6c1a679985d2244e` |
| I-085 | `incident-uq` | 70 | да | — | `ed55dd1d5ae9481c` |
| I-086 | `incident` | 69 | да | 73, 75 | `06a29c2d292d3f8c` |
| I-086 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-087 | `incident` | 71 | да | — | `8671a33a83e481c9` |
| I-087 | `incident-uq` | 102 | да | — | `57990ae5b3ef2b88` |
| I-088 | `incident` | 71 | да | 69 | `42b5babc960cc7d8` |
| I-088 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-089 | `incident` | 71 | да | 69 | `4d4e52e4ddd5b098` |
| I-089 | `incident-uq` | 72 | да | — | `bfa40345df872e6b` |
| I-090 | `incident` | 71 | да | 0, 5, 11, 25, 31, 61, 69, 85 | `e545a5af59c65dba` |
| I-090 | `incident-uq` | 78 | да | — | `d0f11ddf4a2ee136` |
| I-091 | `incident` | 73 | да | 75, 76 | `cbae9297416d4153` |
| I-091 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-092 | `incident` | 73 | да | 75, 76 | `cbae9297416d4153` |
| I-093 | `incident` | 73 | да | 75 | `de4aab458e2628e4` |
| I-093 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-094 | `incident` | 73 | да | 75 | `1a0142c106ff77fd` |
| I-095 | `incident` | 73 | да | 75 | `48a629b37eed5af8` |
| I-095 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-096 | `incident` | 73 | да | — | `270c9ddaf87d0bd8` |
| I-096 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-097 | `incident` | 73 | да | 75 | `28483e6f3496213b` |
| I-097 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-098 | `incident` | 73 | да | — | `a80f2a98485dfb8a` |
| I-098 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-099 | `incident` | 73 | да | — | `1cd3fef693105021` |
| I-100 | `incident` | 73 | да | 75 | `4fdbef857b0f2e76` |
| I-100 | `incident-uq` | 76 | да | — | `dc7dbb30d84eab62` |
| I-101 | `incident` | 75 | да | — | `397d4b529bdd8798` |
| I-102 | `incident` | 75 | да | 51, 73, 76, 77, 101 | `32fd6f051ca87f40` |
| I-102 | `incident-uq` | 76 | да | 73, 75 | `ea4a79d0ec637706` |
| I-103 | `incident` | 75 | да | 51, 73, 76, 77, 101 | `32fd6f051ca87f40` |
| I-104 | `incident` | 77 | да | — | `5fed287899e13f1b` |
| I-105 | `incident` | 77 | да | 78, 79 | `fbbad99639a5945b` |
| I-105 | `incident-uq` | 78 | да | — | `047adce115b2e910` |
| I-106 | `incident` | 77 | да | 78, 79, 81 | `bedfac32417ad81c` |
| I-106 | `incident-uq` | 78 | да | — | `0abf64215e72c9a0` |
| I-107 | `incident` | 77 | да | 79 | `0730c45bd9b2e69f` |
| I-107 | `incident-uq` | 78 | да | — | `d0f11ddf4a2ee136` |
| I-108 | `incident` | 77 | да | 78, 79, 81, 83 | `d8ea66da372112ab` |
| I-108 | `incident-uq` | 78 | да | — | `002eb2245c2b2d96` |
| I-109 | `incident` | 77 | да | 63, 78, 79 | `225e487877e8dda2` |
| I-109 | `incident-uq` | 78 | да | — | `a3c9608e59c263d5` |
| I-110 | `incident` | 77 | да | — | `27bc6a6b21f446ee` |
| I-110 | `incident-uq` | 78 | да | — | `3fc47213d7d61c0b` |
| I-111 | `incident` | 77 | да | 25, 78, 79 | `77b591eeb0dafac4` |
| I-111 | `incident-uq` | 78 | да | — | `3c0db24ff306baf8` |
| I-112 | `incident` | 77 | да | 87, 91, 104 | `2d926a34d2e5b53a` |
| I-112 | `incident-uq` | 78 | да | — | `f8241879687ea3d8` |
| I-113 | `incident` | 77 | да | — | `ca9aa4b7f1a0b809` |
| I-113 | `incident-uq` | 78 | да | — | `91989b5ce41bbabb` |
| I-114 | `incident` | 77 | да | — | `47b48213aecdb796` |
| I-115 | `incident` | 77 | да | — | `537e3d3e8d2582e9` |
| I-116 | `incident` | 79 | да | 81, 82 | `3a31fc6851801caf` |
| I-116 | `incident-uq` | 82 | да | — | `878dd1e5c1f4218c` |
| I-117 | `incident` | 79 | да | 81, 82 | `c6969991b88510fb` |
| I-117 | `incident-uq` | 82 | да | — | `d6db92995b803d5c` |
| I-118 | `incident` | 79 | да | 77 | `09598554d7b3957c` |
| I-118 | `incident-uq` | 82 | да | — | `ed3ef97d08c4b554` |
| I-119 | `incident` | 81 | да | — | `005a89d37fa60f52` |
| I-120 | `incident` | 81 | да | — | `c6b81a16aa5260df` |
| I-121 | `incident` | 83 | да | 79, 81, 84 | `4d1ed51c6e1bab62` |
| I-121 | `incident-uq` | 84 | да | — | `87072eba6f9c95c9` |
| I-122 | `incident` | 83 | да | 84 | `13e412babd1a9c09` |
| I-122 | `incident-uq` | 84 | да | — | `ab841d1954f0a456` |
| I-123 | `incident` | 83 | да | — | `5004b0596c3ff0a2` |
| I-123 | `incident-uq` | 84 | да | — | `0b4ce489a22525de` |
| I-124 | `incident` | 85 | да | — | `db6b72113d0c7460` |
| I-125 | `incident` | 85 | да | — | `4a6c824e37fcbe9f` |
| I-126 | `incident` | 85 | да | — | `8cd6b0ba5a24b466` |
| I-127 | `incident` | 85 | да | — | `605b01ae0e323b15` |
| I-128 | `incident` | 87 | да | 88, 89 | `a219cdad9b806b7f` |
| I-129 | `incident` | 93 | да | — | `da17cf0a32276979` |
| I-129 | `incident-uq` | 100 | да | — | `ea0fc2d4bd5337f7` |
| I-130 | `incident` | 93 | да | — | `92aa5aaffa69cf14` |
| I-130 | `incident-uq` | 100 | да | — | `27cbd1a786210b32` |
| I-131 | `incident` | 93 | да | — | `bc6d740b712e2114` |
| I-131 | `incident-uq` | 100 | да | — | `ea0fc2d4bd5337f7` |
| I-132 | `incident` | 93 | да | — | `1c8bffb83cce877d` |
| I-133 | `incident` | 93 | да | — | `0f2f29a12e4512fa` |
| I-134 | `incident` | 93 | да | — | `bb4d414e756349bf` |
| I-135 | `incident` | 93 | да | — | `97f086a697a7a212` |
| I-135 | `incident-uq` | 94 | да | — | `b7682d66967126fa` |
| I-136 | `incident` | 99 | да | — | `50b165da7c21bedc` |
| I-137 | `incident` | 101 | да | — | `7d807a8f6a9ed293` |
| I-138 | `incident` | 101 | да | — | `363eeab07696f515` |
| I-139 | `incident` | 103 | да | — | `12d86274ed6868c9` |
| I-140 | `incident` | 103 | да | — | `8d93e9c1f1470c1c` |
| I-141 | `incident` | 103 | да | — | `5997d68377242b24` |
| I-142 | `incident` | 103 | да | — | `73597ebb386e837e` |
| I-143 | `incident` | 103 | да | — | `c5582b5b149ecd04` |
| I-144 | `incident` | 103 | да | — | `99ea7b63f05cd455` |
| I-145 | `incident` | 103 | да | — | `4725ed75c0a8c592` |
| I-146 | `incident` | 103 | да | — | `55bc84577de8b97a` |
| I-147 | `incident` | 103 | да | — | `2867088d80ceb801` |
| I-148 | `incident` | 103 | да | — | `821efec648be1681` |
| I-149 | `incident` | 103 | да | — | `d866bfefedaf5fa7` |
| N-01 | `negative` | 11 | да | — | `adce762407090ba4` |
| N-02 | `negative` | 13 | да | — | `1d48fdfe2b244ac7` |
| N-03 | `negative` | 17 | да | — | `c880d95eba7392c9` |
| N-04 | `negative` | 23 | да | — | `f82c702c6cdc36ed` |
| N-04 | `negative-uq` | 24 | да | 104 | `1694ff8345e71165` |
| N-05 | `negative` | 39 | да | — | `66fee4bc8c7e984c` |
| N-06 | `negative` | 79 | да | — | `e60923565c95606e` |
| N-07 | `negative` | 85 | да | 86 | `b287d8cc6bbfc0d3` |
| N-07 | `negative-uq` | 86 | да | — | `7d9768a303c2627e` |
| N-08 | `negative` | 89 | да | — | `94891d68df244bcd` |
| N-08 | `negative-uq` | 90 | да | — | `996dccd410b2f7bc` |
| N-09 | `negative` | 97 | да | — | `65876cdf7b54e5fe` |
| N-10 | `negative` | 99 | да | — | `010237b37fc5f557` |
| N-10 | `negative-uq` | 104 | да | — | `a954538962a0edec` |
| N-11 | `negative` | 101 | да | — | `ec310e61ea21e40c` |
| N-12 | `negative` | 101 | да | — | `3a0c91dbaa6a5adc` |
| SC-01 | `success` | 6 | да | — | `a42c684a0dc13d4f` |
| SC-02 | `success` | 6 | да | — | `fb72e725ae02b288` |
| SC-03 | `success` | 26 | да | — | `3a34306e8a3d35c0` |
| SC-04 | `success` | 26 | да | — | `de9ac773c3a9e07a` |
| SC-05 | `success` | 38 | да | — | `06b181d1755dc82e` |
| SC-06 | `success` | 60 | да | — | `5eac20ddd807a3fc` |
| SC-07 | `success` | 74 | да | — | `f61b26ad799c74f8` |
| SC-08 | `success` | 78 | да | — | `0abf64215e72c9a0` |
| SC-09 | `success` | 78 | да | — | `d0f11ddf4a2ee136` |
| SC-10 | `success` | 70 | да | — | `630c11117a8f8fd5` |
| SC-11 | `success` | 100 | да | — | `ea0fc2d4bd5337f7` |
| SC-12 | `success` | 100 | да | — | `7c4d761dd73a675b` |
| SC-13 | `success` | 104 | да | 22, 24 | `3fe876e6e2ffcd2e` |
| SC-14 | `success` | 104 | да | 22, 24, 25 | `d4fafcee9d8d5b27` |
| SC-15 | `success` | 104 | да | 35, 37, 46, 47, 54 | `93cef5a826961db6` |
| SC-16 | `success` | 104 | да | 37, 43, 45, 47, 54 | `a5b0c367ca575027` |
| SC-17 | `success` | 104 | да | 79, 81, 83, 85, 87, 91 | `a3ed802bdcb77879` |
| SC-18 | `success` | 104 | да | 89, 91 | `8d1c1f13a13066d3` |
| SC-19 | `success` | 104 | да | 6, 81, 83, 87, 91 | `db4d97b5d2fb004f` |
| SC-20 | `success` | 104 | да | 87, 91 | `27bcc6f565ee4620` |
| SC-21 | `success` | 104 | да | 87, 91 | `4c35ec8b3f99ccbc` |
| SC-22 | `success` | 104 | да | 79, 81, 83, 85, 87, 91 | `e5fd0c9e13fe6ca4` |
