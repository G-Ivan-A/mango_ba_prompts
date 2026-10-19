---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/375"
related_artifacts:
  - "experiments/issue_375_verify_quotes.py"
---

# Журнал сверки цитат прогона RUN-0074

> Файл **порождён** скриптом [`experiments/issue_375_golden_set.py`](../../../../experiments/issue_375_golden_set.py) из вывода [`experiments/issue_375_verify_quotes.py`](../../../../experiments/issue_375_verify_quotes.py) — не редактируйте вручную.

Каждая цитата разметки искалась в тексте заявленной реплики экспорта после нормализации (пробелы схлопнуты, `*` и `` ` `` удалены). Текст экспорта в журнал не копируется: фиксируется SHA-256 нормализованной цитаты.

- SHA-256 экспорта: `5eddd393276aa3e6e95088d2cf5bacb7464aee22da2cf5b3ce6b4f5da87f54b7`
- Реплик в ветке: 214
- Цитат проверено: 324; не найдено в заявленной реплике: **0**
- Встречаются ещё и в других репликах: 52 (заявленная реплика входит в список найденных — привязка однозначна по номеру реплики)

| Вид цитаты | Проверено |
| --- | --- |
| `incident` | 193 |
| `incident-uq` | 86 |
| `negative` | 14 |
| `negative-uq` | 3 |
| `success` | 28 |

| Ссылка | Вид | Реплика | Найдена | Также в репликах | SHA-256 (нормализованной) |
| --- | --- | --- | --- | --- | --- |
| I-001 | `incident` | 0 | да | — | `8d19c1f3fcac6553` |
| I-001 | `incident-uq` | 80 | да | — | `7c266b2d4ce51da6` |
| I-002 | `incident` | 0 | да | — | `7402a5671ac7037a` |
| I-002 | `incident-uq` | 52 | да | — | `17209bafc4235faa` |
| I-003 | `incident` | 0 | да | — | `5bfd814e52e0410d` |
| I-004 | `incident` | 3 | да | — | `e2581348fee30484` |
| I-004 | `incident-uq` | 4 | да | — | `935c98aa210b411c` |
| I-005 | `incident` | 3 | да | — | `ef0d84ce8be8306f` |
| I-006 | `incident` | 7 | да | — | `8ff14304277b329a` |
| I-006 | `incident-uq` | 8 | да | — | `3bfa97370da0bb65` |
| I-007 | `incident` | 7 | да | — | `8cd7fe78d1384743` |
| I-007 | `incident-uq` | 8 | да | — | `3bfa97370da0bb65` |
| I-008 | `incident` | 9 | да | — | `2a978c962315d9c3` |
| I-009 | `incident` | 13 | да | — | `395c8b1548bed286` |
| I-009 | `incident-uq` | 14 | да | — | `8da3a3b291b46d24` |
| I-010 | `incident` | 13 | да | — | `4866dfe2a8944a03` |
| I-010 | `incident-uq` | 16 | да | — | `207a5c9aa6462ed5` |
| I-011 | `incident` | 13 | да | 14, 15 | `e40fafc0511b22a5` |
| I-012 | `incident` | 15 | да | — | `7abfe0bc809b2ef3` |
| I-012 | `incident-uq` | 16 | да | — | `207a5c9aa6462ed5` |
| I-013 | `incident` | 15 | да | — | `07b77ac7c6592d8f` |
| I-014 | `incident` | 15 | да | — | `aad39d53b4a84999` |
| I-015 | `incident` | 15 | да | — | `21edc4f1d0eff624` |
| I-016 | `incident` | 15 | да | 16 | `c6ec65919c060b2a` |
| I-017 | `incident` | 15 | да | — | `51d63545f5b5205a` |
| I-018 | `incident` | 15 | да | — | `b65c08acc3c04425` |
| I-019 | `incident` | 19 | да | — | `2ecc8f6e79fab627` |
| I-019 | `incident-uq` | 22 | да | — | `eaa8aa0c12f4e538` |
| I-020 | `incident` | 19 | да | — | `1ed1c51b6ac57a36` |
| I-020 | `incident-uq` | 20 | да | — | `3fc82dc48773ad87` |
| I-021 | `incident` | 21 | да | — | `bc07d2772a7f6375` |
| I-021 | `incident-uq` | 22 | да | — | `eaa8aa0c12f4e538` |
| I-022 | `incident` | 25 | да | — | `6c7d63bb85371fa2` |
| I-022 | `incident-uq` | 26 | да | — | `7e8b704916589e42` |
| I-023 | `incident` | 25 | да | — | `21b861cc6144b933` |
| I-023 | `incident-uq` | 26 | да | — | `7e8b704916589e42` |
| I-024 | `incident` | 25 | да | — | `bce2dcea04a0176b` |
| I-024 | `incident-uq` | 26 | да | — | `7e8b704916589e42` |
| I-025 | `incident` | 27 | да | — | `de359fb2c3c4e742` |
| I-025 | `incident-uq` | 28 | да | — | `cd454c43bb4e6836` |
| I-026 | `incident` | 27 | да | — | `2077023bde2c0afa` |
| I-027 | `incident` | 29 | да | — | `d211f39f0cc129a4` |
| I-028 | `incident` | 35 | да | — | `4ccbf5dca1c98d5c` |
| I-029 | `incident` | 37 | да | — | `7db259ba51f2a520` |
| I-030 | `incident` | 39 | да | — | `16bd4f8d090ae8ef` |
| I-031 | `incident` | 39 | да | — | `4e88cb2833dcb735` |
| I-031 | `incident-uq` | 56 | да | — | `e81e2b7094627dd4` |
| I-032 | `incident` | 39 | да | — | `8bfc6c0c31479e97` |
| I-032 | `incident-uq` | 40 | да | — | `ec8a23bacce2bd83` |
| I-033 | `incident` | 39 | да | — | `d3ce2b4158572198` |
| I-034 | `incident` | 41 | да | 43 | `f72cc575bba6ae9a` |
| I-034 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-035 | `incident` | 41 | да | 43 | `f72cc575bba6ae9a` |
| I-035 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-036 | `incident` | 41 | да | — | `05143b4e35f09c33` |
| I-036 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-037 | `incident` | 41 | да | 42 | `256d5ad7724ed62c` |
| I-037 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-038 | `incident` | 41 | да | 42 | `63d1a704588ee6fe` |
| I-038 | `incident-uq` | 42 | да | — | `8a4252e84f0ce3a1` |
| I-039 | `incident` | 41 | да | — | `ebd7f5d3a3ba81d0` |
| I-039 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-040 | `incident` | 41 | да | 42, 147, 151, 187 | `885d4bbf3962b4ce` |
| I-040 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-041 | `incident` | 41 | да | — | `eece90812fe0df7a` |
| I-041 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-042 | `incident` | 41 | да | — | `fd1726efb6d62098` |
| I-042 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-043 | `incident` | 41 | да | — | `5aa045104141fed7` |
| I-043 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-044 | `incident` | 41 | да | — | `eebc68f7f7737abe` |
| I-044 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-045 | `incident` | 41 | да | — | `9522329876630554` |
| I-045 | `incident-uq` | 42 | да | — | `526483ac3f417783` |
| I-046 | `incident` | 41 | да | 42 | `7d059263ee68502c` |
| I-046 | `incident-uq` | 42 | да | — | `c2c0a8f0ad035362` |
| I-047 | `incident` | 43 | да | — | `b5fe576477ca786e` |
| I-048 | `incident` | 43 | да | — | `0a39804d800ae8ef` |
| I-049 | `incident` | 45 | да | — | `a4533c45b6dae57b` |
| I-050 | `incident` | 47 | да | 48 | `9b0dc1b34bfd6657` |
| I-050 | `incident-uq` | 48 | да | — | `9663448ef23af67b` |
| I-051 | `incident` | 47 | да | — | `3321f8d4e8f9762d` |
| I-051 | `incident-uq` | 48 | да | — | `d312992d7fdbeef7` |
| I-052 | `incident` | 51 | да | — | `06dafb047c542b3f` |
| I-052 | `incident-uq` | 52 | да | — | `17209bafc4235faa` |
| I-053 | `incident` | 51 | да | 52 | `9a6ac19aa6ed75ff` |
| I-053 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-054 | `incident` | 51 | да | — | `ab1393bbdbbd37b8` |
| I-054 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-055 | `incident` | 51 | да | — | `69ebe68462be92e9` |
| I-055 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-056 | `incident` | 51 | да | — | `927e41ed7592f498` |
| I-056 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-057 | `incident` | 51 | да | — | `d77d2f0976929a2e` |
| I-057 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-058 | `incident` | 51 | да | — | `d6bc489a562c4598` |
| I-058 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-059 | `incident` | 51 | да | — | `39456bc55f245733` |
| I-059 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-060 | `incident` | 51 | да | — | `d30ae2491ea83cb8` |
| I-060 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-061 | `incident` | 51 | да | — | `cdfb0b3425f4211c` |
| I-061 | `incident-uq` | 52 | да | — | `86a5e6aa7b0d29c2` |
| I-062 | `incident` | 51 | да | — | `83f5de9654a4e145` |
| I-062 | `incident-uq` | 52 | да | — | `d8b8fafb33912048` |
| I-063 | `incident` | 53 | да | 57 | `2710e314407d57d8` |
| I-063 | `incident-uq` | 56 | да | — | `e81e2b7094627dd4` |
| I-064 | `incident` | 55 | да | — | `03d708c7e8bf9b6d` |
| I-065 | `incident` | 55 | да | — | `2bfaadad4591a717` |
| I-066 | `incident` | 55 | да | — | `03d81edde7efad25` |
| I-067 | `incident` | 57 | да | — | `d892122bd6a3bdc4` |
| I-068 | `incident` | 61 | да | 62 | `7d4c9a56840e2d92` |
| I-068 | `incident-uq` | 62 | да | — | `e7b147d109f19630` |
| I-069 | `incident` | 61 | да | 63, 67 | `39930ac71e3495ea` |
| I-069 | `incident-uq` | 62 | да | — | `e7b147d109f19630` |
| I-070 | `incident` | 61 | да | — | `4eafc12f572bb642` |
| I-070 | `incident-uq` | 62 | да | — | `e7b147d109f19630` |
| I-071 | `incident` | 61 | да | — | `fa2275ad4f8e50a3` |
| I-071 | `incident-uq` | 62 | да | — | `4e9b29c97c3ee308` |
| I-072 | `incident` | 61 | да | — | `dfdfe560ec14cdcc` |
| I-073 | `incident` | 61 | да | 62 | `911d9702ec06924e` |
| I-073 | `incident-uq` | 62 | да | — | `eeb6d0ab2a6de296` |
| I-074 | `incident` | 61 | да | 62 | `552b1dfaa2fdd7de` |
| I-074 | `incident-uq` | 62 | да | — | `9854c1383c85b14b` |
| I-075 | `incident` | 61 | да | — | `9624fc96d6973a7a` |
| I-075 | `incident-uq` | 62 | да | — | `28821a160b758221` |
| I-076 | `incident` | 63 | да | — | `d040bf585c421f56` |
| I-076 | `incident-uq` | 64 | да | — | `ced67fa32b8c1972` |
| I-077 | `incident` | 63 | да | — | `0e8cdd05f52b764d` |
| I-078 | `incident` | 63 | да | 67 | `79c3b231734b492a` |
| I-078 | `incident-uq` | 70 | да | — | `598ea55feb66983b` |
| I-079 | `incident` | 67 | да | — | `fc72dae251a6a22f` |
| I-080 | `incident` | 67 | да | 70 | `e4254fb3aca69a82` |
| I-080 | `incident-uq` | 70 | да | — | `43b18c9778d0ab16` |
| I-081 | `incident` | 67 | да | 70 | `07cccf6ddee7c049` |
| I-081 | `incident-uq` | 70 | да | — | `43b18c9778d0ab16` |
| I-082 | `incident` | 67 | да | 70 | `44c7f23b4fcbdece` |
| I-082 | `incident-uq` | 70 | да | — | `43b18c9778d0ab16` |
| I-083 | `incident` | 67 | да | 63 | `ca3c9742761a2e93` |
| I-083 | `incident-uq` | 70 | да | — | `8469aa9b006bb50d` |
| I-084 | `incident` | 67 | да | 63 | `79c3b231734b492a` |
| I-084 | `incident-uq` | 70 | да | — | `598ea55feb66983b` |
| I-085 | `incident` | 69 | да | — | `6c5600b9e3d1b904` |
| I-085 | `incident-uq` | 80 | да | — | `7c266b2d4ce51da6` |
| I-086 | `incident` | 71 | да | — | `c941240c60fa2722` |
| I-087 | `incident` | 71 | да | 67, 70 | `d0f4521823e66e80` |
| I-087 | `incident-uq` | 72 | да | — | `48fbc6c69742196f` |
| I-088 | `incident` | 73 | да | — | `883a3569de47bb28` |
| I-089 | `incident` | 73 | да | 92, 93 | `043f5ff986850d57` |
| I-090 | `incident` | 73 | да | 93 | `a89e811262b09c03` |
| I-091 | `incident` | 75 | да | — | `c28be12ef8a29ab5` |
| I-092 | `incident` | 75 | да | — | `4c67b783e4dd5875` |
| I-093 | `incident` | 75 | да | — | `e67e593b35750442` |
| I-094 | `incident` | 79 | да | 80 | `5bd5d7adce455fc7` |
| I-094 | `incident-uq` | 80 | да | — | `7c266b2d4ce51da6` |
| I-095 | `incident` | 79 | да | — | `686aef7dff1ee9f7` |
| I-095 | `incident-uq` | 80 | да | — | `7c266b2d4ce51da6` |
| I-096 | `incident` | 79 | да | — | `482e2389d5547d89` |
| I-096 | `incident-uq` | 80 | да | — | `7c266b2d4ce51da6` |
| I-097 | `incident` | 79 | да | — | `5601ea1b23d32436` |
| I-097 | `incident-uq` | 80 | да | — | `7c266b2d4ce51da6` |
| I-098 | `incident` | 79 | да | — | `ef29961b4ddca176` |
| I-098 | `incident-uq` | 80 | да | — | `7c266b2d4ce51da6` |
| I-099 | `incident` | 79 | да | — | `77aec3c4215a75d8` |
| I-099 | `incident-uq` | 80 | да | — | `c2564f1982520f42` |
| I-100 | `incident` | 81 | да | — | `ffcf7bba6d2451c4` |
| I-101 | `incident` | 83 | да | — | `44c9029fde356536` |
| I-101 | `incident-uq` | 84 | да | — | `9d3f0ecd17d2288a` |
| I-102 | `incident` | 83 | да | — | `a66447976ba625a5` |
| I-102 | `incident-uq` | 84 | да | — | `9d3f0ecd17d2288a` |
| I-103 | `incident` | 83 | да | 84, 91, 92, 93, 116 | `65b819a45a05044d` |
| I-104 | `incident` | 83 | да | 84 | `2d1392da4196fa3d` |
| I-105 | `incident` | 83 | да | 84 | `04d85bba1b597721` |
| I-106 | `incident` | 83 | да | 84 | `7a177b610d220b82` |
| I-107 | `incident` | 85 | да | — | `823e944ba0b3aba7` |
| I-108 | `incident` | 85 | да | — | `7af22e57384857d0` |
| I-109 | `incident` | 87 | да | — | `7c0315180f64804d` |
| I-110 | `incident` | 89 | да | — | `d2f4ea7990117661` |
| I-111 | `incident` | 89 | да | — | `65836ef5d18d2df1` |
| I-112 | `incident` | 91 | да | — | `e13784e6e0f5d86c` |
| I-113 | `incident` | 93 | да | 129, 197 | `17b8241dc7ee9308` |
| I-114 | `incident` | 93 | да | — | `a7248ba39d9a11f7` |
| I-114 | `incident-uq` | 94 | да | — | `7ceea053b31a5c2b` |
| I-115 | `incident` | 93 | да | — | `0df732599467ad5f` |
| I-115 | `incident-uq` | 94 | да | — | `7ceea053b31a5c2b` |
| I-116 | `incident` | 107 | да | — | `34007c54a72cc81b` |
| I-116 | `incident-uq` | 108 | да | — | `fff4ef410967c0c8` |
| I-117 | `incident` | 107 | да | — | `4de77e23cb5e3049` |
| I-117 | `incident-uq` | 108 | да | — | `fff4ef410967c0c8` |
| I-118 | `incident` | 111 | да | — | `3481ea158d825157` |
| I-119 | `incident` | 113 | да | — | `9d5b2a4e21c36a99` |
| I-120 | `incident` | 113 | да | 91, 92, 93, 116, 119, 121, 123, 127, 211, 212, 213 | `c166dd92e2cac55e` |
| I-120 | `incident-uq` | 114 | да | — | `040467336059a99e` |
| I-121 | `incident` | 113 | да | — | `f95524e08e7e0c6f` |
| I-122 | `incident` | 115 | да | — | `971d4dd2e5779f8f` |
| I-122 | `incident-uq` | 118 | да | — | `3067ede07ba059f3` |
| I-123 | `incident` | 115 | да | — | `2638b33e0ec91f0a` |
| I-123 | `incident-uq` | 118 | да | — | `3067ede07ba059f3` |
| I-124 | `incident` | 115 | да | — | `d3097b1e91ae6d34` |
| I-125 | `incident` | 115 | да | — | `91ec628caefe93dd` |
| I-126 | `incident` | 115 | да | — | `2020ffc624a3bc69` |
| I-127 | `incident` | 117 | да | — | `eb3dcc8928066c72` |
| I-128 | `incident` | 117 | да | — | `ce7aa82ed70f7f8d` |
| I-129 | `incident` | 119 | да | — | `f12054176d027a36` |
| I-130 | `incident` | 119 | да | — | `74d38cf701befa44` |
| I-131 | `incident` | 119 | да | — | `01bfc0b5997251b5` |
| I-132 | `incident` | 119 | да | 61, 63, 67, 70, 71, 73, 75, 79, 83, 84, 85, 91, 92, 93, 97, 101, 112, 113, 115, 116, 121, 123, 127, 128, 141, 144, 145, 158, 159, 160, 161, 164, 165, 167, 171, 175, 176, 177, 182, 183, 184, 185, 190, 196, 197, 200, 203, 207 | `3dc9cee2897055a2` |
| I-132 | `incident-uq` | 122 | да | — | `1e472084498ff4c1` |
| I-133 | `incident` | 119 | да | 120 | `72941056539eceff` |
| I-134 | `incident` | 119 | да | 120 | `73aeef8c28979a32` |
| I-135 | `incident` | 121 | да | — | `8aea503239abadcb` |
| I-136 | `incident` | 121 | да | — | `a39750613f56c169` |
| I-137 | `incident` | 121 | да | — | `fd758ce5a5bdbd37` |
| I-138 | `incident` | 121 | да | 119, 127 | `78c078941b1d4e14` |
| I-139 | `incident` | 121 | да | 128, 144, 145, 158, 159, 160, 161, 164, 182, 183 | `d385b8d20a159dcf` |
| I-140 | `incident` | 121 | да | 61, 63, 67, 70, 71, 73, 75, 79, 83, 84, 85, 91, 92, 93, 97, 101, 112, 113, 115, 116, 119, 123, 127, 128, 141, 144, 145, 158, 159, 160, 161, 164, 165, 167, 171, 175, 176, 177, 182, 183, 184, 185, 190, 196, 197, 200, 203, 207 | `3dc9cee2897055a2` |
| I-140 | `incident-uq` | 122 | да | — | `075c06789b106e4f` |
| I-141 | `incident` | 123 | да | — | `380a395ca78785c2` |
| I-142 | `incident` | 123 | да | — | `a2056a84fc8c7f6b` |
| I-143 | `incident` | 123 | да | — | `e9b07da26adbdc4d` |
| I-144 | `incident` | 127 | да | — | `f46e0310785d77c1` |
| I-145 | `incident` | 127 | да | 121, 128, 164, 167, 184, 190 | `465c638e0babcd44` |
| I-146 | `incident` | 129 | да | — | `62556a5b22e5ce24` |
| I-147 | `incident` | 129 | да | — | `f7c3013fbe40e31b` |
| I-148 | `incident` | 129 | да | — | `b09fce3ccbb03cd1` |
| I-149 | `incident` | 131 | да | — | `76a744b0b4accd17` |
| I-150 | `incident` | 133 | да | — | `ba18a98ed0223b51` |
| I-150 | `incident-uq` | 134 | да | — | `15afbfad7f06df24` |
| I-151 | `incident` | 133 | да | — | `a5b6771df9e12661` |
| I-152 | `incident` | 135 | да | — | `a1955179eb1c7ad4` |
| I-153 | `incident` | 137 | да | — | `a27c6478388964d0` |
| I-154 | `incident` | 137 | да | — | `65fea5c629c9b1bb` |
| I-155 | `incident` | 139 | да | — | `741ab94568ac66f6` |
| I-155 | `incident-uq` | 140 | да | — | `f2df96c728db8311` |
| I-156 | `incident` | 139 | да | 140 | `97573b0371c84fcb` |
| I-156 | `incident-uq` | 140 | да | — | `cdcddcafb8885a7d` |
| I-157 | `incident` | 139 | да | — | `84f84f535bdde14c` |
| I-158 | `incident` | 141 | да | — | `1e5135bce1a5e2ab` |
| I-159 | `incident` | 141 | да | — | `7846a52fcf277561` |
| I-160 | `incident` | 143 | да | — | `bbcbe31034d2ff9c` |
| I-161 | `incident` | 143 | да | 145, 159, 161, 165, 179, 185, 203, 207 | `9a6031178dd0b9cb` |
| I-162 | `incident` | 147 | да | — | `f2a341688d583f37` |
| I-163 | `incident` | 149 | да | 65, 119, 123, 135, 143 | `182d793fa2d713b4` |
| I-164 | `incident` | 153 | да | — | `0886acf12a07a255` |
| I-165 | `incident` | 153 | да | — | `cf6facb29e4ecd31` |
| I-166 | `incident` | 153 | да | 156 | `9648b2db092be181` |
| I-166 | `incident-uq` | 156 | да | — | `e72b9dbe4fec81c7` |
| I-167 | `incident` | 155 | да | — | `889c332f87168659` |
| I-168 | `incident` | 155 | да | — | `42698baa017f901e` |
| I-169 | `incident` | 155 | да | — | `8a6c5af9ac8cfc3d` |
| I-170 | `incident` | 157 | да | 159, 163 | `021e357f4a2c38c3` |
| I-171 | `incident` | 161 | да | — | `0d30face7fe5b906` |
| I-172 | `incident` | 165 | да | — | `b8de856bf0c9fd4b` |
| I-173 | `incident` | 169 | да | — | `c0fb9d5fc02192c6` |
| I-174 | `incident` | 173 | да | 87 | `5fbcb23ee29f8681` |
| I-174 | `incident-uq` | 174 | да | — | `deb1e8d7c41d1bcf` |
| I-175 | `incident` | 185 | да | — | `1122e6757982a489` |
| I-176 | `incident` | 187 | да | — | `769622a53b31a818` |
| I-176 | `incident-uq` | 188 | да | — | `fa3601e0bee3c31f` |
| I-177 | `incident` | 191 | да | 197 | `4133a394093d285a` |
| I-178 | `incident` | 191 | да | 197, 201 | `5b3d9fbe252ef393` |
| I-179 | `incident` | 191 | да | 197 | `6464b95593feaec8` |
| I-180 | `incident` | 191 | да | — | `6ec50399e6beb8e8` |
| I-181 | `incident` | 193 | да | — | `87f523ce1a51c2dd` |
| I-181 | `incident-uq` | 194 | да | — | `edde39fbbd80902f` |
| I-182 | `incident` | 193 | да | — | `b998773482743152` |
| I-183 | `incident` | 195 | да | — | `2aae99df68079a20` |
| I-184 | `incident` | 197 | да | — | `0fb516248e8f253b` |
| I-185 | `incident` | 199 | да | — | `2d88523c76002024` |
| I-186 | `incident` | 201 | да | — | `87a11bf9ea4930f7` |
| I-187 | `incident` | 205 | да | 207 | `d92251cf8d8bc1cf` |
| I-188 | `incident` | 207 | да | — | `19607417607110ee` |
| I-189 | `incident` | 207 | да | 205 | `2c8fc1645195a48a` |
| I-190 | `incident` | 207 | да | 203 | `7a2a7c465174b4a0` |
| I-191 | `incident` | 211 | да | — | `b3dc823a6be68412` |
| I-191 | `incident-uq` | 212 | да | — | `509f6bac8cbfb65e` |
| I-192 | `incident` | 211 | да | — | `bad4ab25490e01a3` |
| I-192 | `incident-uq` | 212 | да | — | `509f6bac8cbfb65e` |
| I-193 | `incident` | 213 | да | — | `bacd0d4306469e64` |
| N-01 | `negative` | 59 | да | — | `b89ec42f4eb25d72` |
| N-02 | `negative` | 65 | да | — | `1c152b3dbabfe3c6` |
| N-02 | `negative-uq` | 66 | да | — | `929e2ea8f1410f32` |
| N-03 | `negative` | 95 | да | — | `26b8a77972c2d6e6` |
| N-04 | `negative` | 109 | да | — | `46c11d5a1ccdfafe` |
| N-04 | `negative-uq` | 110 | да | — | `91cbe6dc9c471416` |
| N-05 | `negative` | 125 | да | — | `e8a8d9f2a0545dec` |
| N-06 | `negative` | 165 | да | — | `332bd03e3cc5fe64` |
| N-07 | `negative` | 175 | да | — | `51782dfeb36559df` |
| N-08 | `negative` | 181 | да | — | `163a66a37cd2dd45` |
| N-09 | `negative` | 183 | да | — | `4c99ccf01e6e54a4` |
| N-10 | `negative` | 189 | да | — | `e372607607fac210` |
| N-11 | `negative` | 203 | да | 207 | `1a68be43b6b24832` |
| N-12 | `negative` | 203 | да | 207 | `ef0a1712ad973521` |
| N-13 | `negative` | 205 | да | — | `f922100518eb36ea` |
| N-13 | `negative-uq` | 206 | да | — | `3f3c5fcc49dd2c25` |
| N-14 | `negative` | 209 | да | — | `38f5d5027b559dfd` |
| SC-01 | `success` | 8 | да | — | `499c169bdf4a004f` |
| SC-02 | `success` | 16 | да | — | `207a5c9aa6462ed5` |
| SC-03 | `success` | 22 | да | — | `66c026c159d34763` |
| SC-04 | `success` | 42 | да | — | `38c787f774866058` |
| SC-05 | `success` | 48 | да | — | `9663448ef23af67b` |
| SC-06 | `success` | 52 | да | — | `04052eb846cab818` |
| SC-07 | `success` | 52 | да | — | `d8b8fafb33912048` |
| SC-08 | `success` | 56 | да | — | `f9996908c8e6126b` |
| SC-09 | `success` | 62 | да | — | `4e9b29c97c3ee308` |
| SC-10 | `success` | 62 | да | — | `e7b147d109f19630` |
| SC-11 | `success` | 62 | да | — | `eeb6d0ab2a6de296` |
| SC-12 | `success` | 62 | да | — | `28821a160b758221` |
| SC-13 | `success` | 66 | да | — | `929e2ea8f1410f32` |
| SC-14 | `success` | 70 | да | — | `43b18c9778d0ab16` |
| SC-15 | `success` | 70 | да | — | `8469aa9b006bb50d` |
| SC-16 | `success` | 72 | да | — | `48fbc6c69742196f` |
| SC-17 | `success` | 80 | да | — | `7c266b2d4ce51da6` |
| SC-18 | `success` | 84 | да | — | `9d3f0ecd17d2288a` |
| SC-19 | `success` | 110 | да | — | `d99aa682454481b0` |
| SC-20 | `success` | 124 | да | — | `625a1f0c85f4b306` |
| SC-21 | `success` | 140 | да | — | `cdcddcafb8885a7d` |
| SC-22 | `success` | 142 | да | — | `aa8ac7adc66c1ece` |
| SC-23 | `success` | 174 | да | — | `deb1e8d7c41d1bcf` |
| SC-24 | `success` | 186 | да | — | `9b049b29312328cb` |
| SC-25 | `success` | 202 | да | — | `c5cd78a25f54ff59` |
| SC-26 | `success` | 202 | да | — | `4c885f4ce7a97bf4` |
| SC-27 | `success` | 204 | да | — | `b461ef6e3d9c507c` |
| SC-28 | `success` | 210 | да | — | `cc1906ccd827cb00` |
