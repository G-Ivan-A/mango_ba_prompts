---
status: draft
version: 0.1
updated: 2026-10-19
ai-generated: true
type: log
scope: mango-only
related_issues:
  - "https://github.com/G-Ivan-A/mango_ba_prompts/issues/378"
related_artifacts:
  - "experiments/issue_378_verify_quotes.py"
---

# Журнал сверки цитат прогона RUN-0075

> Файл **порождён** скриптом [`experiments/issue_378_golden_set.py`](../../../../experiments/issue_378_golden_set.py) из вывода [`experiments/issue_378_verify_quotes.py`](../../../../experiments/issue_378_verify_quotes.py) — не редактируйте вручную.

Каждая цитата разметки искалась в тексте заявленной реплики экспорта после нормализации (пробелы схлопнуты, `*` и `` ` `` удалены). Текст экспорта в журнал не копируется: фиксируется SHA-256 нормализованной цитаты.

- SHA-256 экспорта: `21b3ac0582bc4c8f28cb99eeb1d687ddf7a0a9685aad669daec39077681dead0`
- Реплик в ветке: 118
- Цитат проверено: 261; не найдено в заявленной реплике: **0**
- Встречаются ещё и в других репликах: 54 (заявленная реплика входит в список найденных — привязка однозначна по номеру реплики)

| Вид цитаты | Проверено |
| --- | --- |
| `incident` | 168 |
| `incident-uq` | 60 |
| `negative` | 9 |
| `negative-uq` | 2 |
| `success` | 22 |

| Ссылка | Вид | Реплика | Найдена | Также в репликах | SHA-256 (нормализованной) |
| --- | --- | --- | --- | --- | --- |
| I-001 | `incident` | 0 | да | 52 | `147b10828d580dfc` |
| I-001 | `incident-uq` | 26 | да | — | `9ebc64af444a9772` |
| I-002 | `incident` | 0 | да | 52, 66 | `8d19c1f3fcac6553` |
| I-003 | `incident` | 0 | да | 52 | `2b131d80f9776594` |
| I-004 | `incident` | 0 | да | 52 | `19f93b26810e8c95` |
| I-005 | `incident` | 0 | да | 52 | `720c418ae4d28b43` |
| I-005 | `incident-uq` | 8 | да | — | `eb75592744c2db11` |
| I-006 | `incident` | 5 | да | 8, 9 | `275dec9bb2e08a02` |
| I-006 | `incident-uq` | 8 | да | — | `e19de6bf0c4d40c4` |
| I-007 | `incident` | 5 | да | — | `3168963f450d8abc` |
| I-007 | `incident-uq` | 8 | да | — | `e19de6bf0c4d40c4` |
| I-008 | `incident` | 5 | да | 8 | `dc859c4c62226b3b` |
| I-009 | `incident` | 7 | да | — | `7e183e87d5475c89` |
| I-009 | `incident-uq` | 26 | да | — | `9ebc64af444a9772` |
| I-010 | `incident` | 7 | да | — | `e39054f1e9849ea0` |
| I-010 | `incident-uq` | 26 | да | — | `9ebc64af444a9772` |
| I-011 | `incident` | 7 | да | — | `54a4ed7f7988e55e` |
| I-011 | `incident-uq` | 26 | да | — | `9ebc64af444a9772` |
| I-012 | `incident` | 7 | да | 0, 9, 52 | `25ad311e3d242b3c` |
| I-013 | `incident` | 11 | да | — | `d9bee27e951a3ae3` |
| I-014 | `incident` | 11 | да | — | `03c9b66839fde002` |
| I-015 | `incident` | 15 | да | — | `098355736422a021` |
| I-016 | `incident` | 17 | да | — | `a48e3d8d3cb7d92a` |
| I-017 | `incident` | 19 | да | 23, 77 | `182d793fa2d713b4` |
| I-018 | `incident` | 19 | да | — | `7aaef5b2618e8916` |
| I-018 | `incident-uq` | 26 | да | — | `38b6583aaba50fe5` |
| I-019 | `incident` | 19 | да | — | `54a3e04437c6d517` |
| I-020 | `incident` | 19 | да | — | `9841f9880616d8f5` |
| I-021 | `incident` | 19 | да | — | `f5206d048d99e37d` |
| I-022 | `incident` | 19 | да | — | `229c3b05c6dd1035` |
| I-022 | `incident-uq` | 26 | да | — | `9ebc64af444a9772` |
| I-023 | `incident` | 21 | да | — | `5485ec3683de5a2b` |
| I-024 | `incident` | 21 | да | 22 | `cde390c292da6bce` |
| I-024 | `incident-uq` | 22 | да | — | `d8fcf58e6a1ff078` |
| I-025 | `incident` | 23 | да | 19, 77 | `182d793fa2d713b4` |
| I-026 | `incident` | 23 | да | — | `ba2cadc9b705d930` |
| I-026 | `incident-uq` | 26 | да | — | `9ebc64af444a9772` |
| I-027 | `incident` | 25 | да | — | `555d04645623af9f` |
| I-027 | `incident-uq` | 26 | да | — | `3754ace4c42f4108` |
| I-028 | `incident` | 25 | да | — | `d3c828fa45e378ef` |
| I-028 | `incident-uq` | 26 | да | — | `9ebc64af444a9772` |
| I-029 | `incident` | 25 | да | 39 | `88b9e326b3942de5` |
| I-030 | `incident` | 25 | да | 26 | `121a1833f19cfcf9` |
| I-030 | `incident-uq` | 26 | да | — | `38b6583aaba50fe5` |
| I-031 | `incident` | 25 | да | — | `a22254d3c6a62afc` |
| I-031 | `incident-uq` | 26 | да | — | `3754ace4c42f4108` |
| I-032 | `incident` | 25 | да | 26 | `f29b37a4911cbf4b` |
| I-032 | `incident-uq` | 26 | да | — | `3754ace4c42f4108` |
| I-033 | `incident` | 27 | да | — | `58f1f707a7c7a1e6` |
| I-034 | `incident` | 27 | да | — | `e31bc5d7f3af87ae` |
| I-035 | `incident` | 27 | да | 28 | `f82c64f2e40c70b7` |
| I-035 | `incident-uq` | 28 | да | — | `1ffd7da22732a3e3` |
| I-036 | `incident` | 29 | да | — | `5f7a9ec0b48864de` |
| I-037 | `incident` | 29 | да | — | `fb8c95c93da5a82c` |
| I-037 | `incident-uq` | 30 | да | — | `39f7a4b69a11af8a` |
| I-038 | `incident` | 31 | да | — | `36761ab06c1dd396` |
| I-039 | `incident` | 31 | да | — | `0151733837c0547f` |
| I-040 | `incident` | 33 | да | — | `7e61bad957f89e84` |
| I-041 | `incident` | 35 | да | — | `5af46b1c0f555908` |
| I-042 | `incident` | 35 | да | — | `8070bd5f85b0ee77` |
| I-042 | `incident-uq` | 50 | да | — | `0e0883f262ff45c4` |
| I-043 | `incident` | 35 | да | — | `ef2b97f6fed02055` |
| I-044 | `incident` | 35 | да | — | `d07c74bacfda1164` |
| I-045 | `incident` | 37 | да | — | `a87dadaaf8f76512` |
| I-045 | `incident-uq` | 50 | да | — | `0e0883f262ff45c4` |
| I-046 | `incident` | 37 | да | — | `7f7c6e5b5d5eaafd` |
| I-047 | `incident` | 37 | да | — | `2eb2ae5e0fe3de74` |
| I-047 | `incident-uq` | 50 | да | — | `0e0883f262ff45c4` |
| I-048 | `incident` | 37 | да | — | `5eafab5dc21d0768` |
| I-049 | `incident` | 39 | да | — | `4a170b07484282c0` |
| I-050 | `incident` | 39 | да | — | `19e2e58e5f5fa221` |
| I-051 | `incident` | 39 | да | — | `025ddb04c864f5a7` |
| I-052 | `incident` | 39 | да | — | `46fd91731422abf4` |
| I-053 | `incident` | 39 | да | — | `cb5c409295befe71` |
| I-054 | `incident` | 41 | да | 42 | `c03546d4cca54245` |
| I-054 | `incident-uq` | 42 | да | — | `8750e2d01b61d780` |
| I-055 | `incident` | 41 | да | — | `93e75aa1fb721c8b` |
| I-056 | `incident` | 41 | да | — | `76dbd7d773e2afde` |
| I-057 | `incident` | 43 | да | — | `8a6cf3fb3d6222ed` |
| I-057 | `incident-uq` | 50 | да | — | `0e0883f262ff45c4` |
| I-058 | `incident` | 43 | да | — | `db9e055a31ab540d` |
| I-059 | `incident` | 43 | да | — | `731d2ff7def7a623` |
| I-060 | `incident` | 43 | да | — | `0bd5110fd5f6c23a` |
| I-060 | `incident-uq` | 50 | да | — | `f496f422509a3056` |
| I-061 | `incident` | 45 | да | — | `1e681869dd6d70f5` |
| I-062 | `incident` | 45 | да | — | `85367e5a33020592` |
| I-063 | `incident` | 45 | да | — | `d67d3d303a8aec36` |
| I-064 | `incident` | 45 | да | — | `9bd0969c834681e2` |
| I-065 | `incident` | 45 | да | — | `706426acff23c507` |
| I-066 | `incident` | 45 | да | — | `a4ed6d39d61376e4` |
| I-067 | `incident` | 47 | да | — | `6f7ad82d5dfb7862` |
| I-067 | `incident-uq` | 48 | да | — | `0a32f639eff80deb` |
| I-068 | `incident` | 47 | да | — | `33c81f94f51b3ac3` |
| I-068 | `incident-uq` | 48 | да | — | `d67336276f29f149` |
| I-069 | `incident` | 47 | да | — | `924b3f06fd92fcd5` |
| I-069 | `incident-uq` | 48 | да | — | `5eb4ee96f0ef751e` |
| I-070 | `incident` | 47 | да | — | `7cc0203ea45b657d` |
| I-070 | `incident-uq` | 48 | да | — | `5eb4ee96f0ef751e` |
| I-071 | `incident` | 47 | да | — | `b9a934d37494da8d` |
| I-072 | `incident` | 47 | да | — | `6b0ce42cc2bd8785` |
| I-072 | `incident-uq` | 48 | да | — | `5eb4ee96f0ef751e` |
| I-073 | `incident` | 47 | да | — | `69b5c3a5fef3a8d0` |
| I-073 | `incident-uq` | 48 | да | — | `5eb4ee96f0ef751e` |
| I-074 | `incident` | 47 | да | — | `ecfea4eadf9ef7b2` |
| I-074 | `incident-uq` | 48 | да | — | `5eb4ee96f0ef751e` |
| I-075 | `incident` | 47 | да | — | `ee4f7935314fd1a5` |
| I-075 | `incident-uq` | 48 | да | — | `5eb4ee96f0ef751e` |
| I-076 | `incident` | 47 | да | — | `92f2725cee8c0576` |
| I-076 | `incident-uq` | 48 | да | — | `5eb4ee96f0ef751e` |
| I-077 | `incident` | 47 | да | — | `4df06650582eed08` |
| I-078 | `incident` | 47 | да | — | `acdf506f47366567` |
| I-079 | `incident` | 49 | да | — | `cbb8c0aae65d3649` |
| I-079 | `incident-uq` | 50 | да | — | `0e0883f262ff45c4` |
| I-080 | `incident` | 49 | да | — | `bc01c27ede615f64` |
| I-081 | `incident` | 49 | да | — | `ccdb8ff40f453849` |
| I-082 | `incident` | 49 | да | — | `4f6387109a07a370` |
| I-083 | `incident` | 49 | да | — | `71e35b134a933d83` |
| I-084 | `incident` | 49 | да | — | `3901ba4257c3b596` |
| I-085 | `incident` | 49 | да | — | `1e3e2805b5726d56` |
| I-086 | `incident` | 51 | да | — | `af99bf393f9881e3` |
| I-087 | `incident` | 51 | да | 52 | `ce77f5f77211fd49` |
| I-088 | `incident` | 51 | да | — | `3a444c3690b7d880` |
| I-089 | `incident` | 51 | да | — | `5ff2a55e3407eac6` |
| I-090 | `incident` | 53 | да | — | `02de84f0b2d62f33` |
| I-090 | `incident-uq` | 54 | да | — | `075e47e0e1281575` |
| I-091 | `incident` | 53 | да | — | `5e3746550406eb73` |
| I-091 | `incident-uq` | 54 | да | — | `075e47e0e1281575` |
| I-092 | `incident` | 53 | да | — | `250e30dff88bc81c` |
| I-092 | `incident-uq` | 64 | да | — | `755b5a708eee6b9d` |
| I-093 | `incident` | 53 | да | 55, 57 | `4e13c1527656a9f4` |
| I-093 | `incident-uq` | 58 | да | — | `583f4820058ea228` |
| I-094 | `incident` | 53 | да | — | `e8f5b33626bccc0e` |
| I-094 | `incident-uq` | 66 | да | — | `c37d1a37057c497c` |
| I-095 | `incident` | 53 | да | — | `8893a96c8488a6d8` |
| I-096 | `incident` | 53 | да | 79 | `2801d52c1aeb16fc` |
| I-097 | `incident` | 53 | да | — | `6d9bc1bd4dda1e2a` |
| I-098 | `incident` | 55 | да | 56 | `971fd440045ac077` |
| I-098 | `incident-uq` | 56 | да | — | `1856195081ab53bc` |
| I-099 | `incident` | 57 | да | — | `0af890199334710e` |
| I-100 | `incident` | 57 | да | 58, 63 | `4b052f442d342b0b` |
| I-101 | `incident` | 57 | да | 53, 55 | `4e13c1527656a9f4` |
| I-101 | `incident-uq` | 58 | да | — | `583f4820058ea228` |
| I-102 | `incident` | 59 | да | — | `f0d771c64777a9e7` |
| I-102 | `incident-uq` | 60 | да | 61 | `7b2fc1393cea7e51` |
| I-103 | `incident` | 59 | да | — | `80f2163f88d70b64` |
| I-103 | `incident-uq` | 60 | да | — | `12349ea39a3f605b` |
| I-104 | `incident` | 59 | да | — | `b279f16ac4db2329` |
| I-104 | `incident-uq` | 60 | да | — | `3f53d740e300ce1e` |
| I-105 | `incident` | 59 | да | — | `7dbe591c443ff594` |
| I-105 | `incident-uq` | 60 | да | 61 | `7b2fc1393cea7e51` |
| I-106 | `incident` | 59 | да | — | `9b903e49e908def8` |
| I-107 | `incident` | 59 | да | — | `3670ab43c04330b1` |
| I-108 | `incident` | 61 | да | — | `73aaf0191a22048d` |
| I-109 | `incident` | 63 | да | — | `7419b651f442e464` |
| I-109 | `incident-uq` | 64 | да | — | `755b5a708eee6b9d` |
| I-110 | `incident` | 63 | да | — | `2d5eafeaa41195be` |
| I-110 | `incident-uq` | 64 | да | — | `755b5a708eee6b9d` |
| I-111 | `incident` | 63 | да | — | `ae79f3153b0cf962` |
| I-111 | `incident-uq` | 64 | да | — | `755b5a708eee6b9d` |
| I-112 | `incident` | 63 | да | 53, 55, 57 | `99847ec4452490e1` |
| I-112 | `incident-uq` | 64 | да | — | `755b5a708eee6b9d` |
| I-113 | `incident` | 66 | да | — | `ab8803c83bb09d9f` |
| I-114 | `incident` | 66 | да | — | `b227a15da74e5668` |
| I-115 | `incident` | 67 | да | — | `f3c8728406349f30` |
| I-116 | `incident` | 67 | да | — | `931ca4017e76b02c` |
| I-117 | `incident` | 67 | да | — | `2558170ac03e8383` |
| I-117 | `incident-uq` | 76 | да | — | `1ebe2e7b6c5779c0` |
| I-118 | `incident` | 69 | да | — | `8f7b54f6ba4a1011` |
| I-119 | `incident` | 71 | да | 73 | `86d4ab0ed67f3e33` |
| I-119 | `incident-uq` | 72 | да | — | `3bb4b10e72aca40e` |
| I-120 | `incident` | 71 | да | 73 | `0342ca2f042be52d` |
| I-121 | `incident` | 71 | да | 73 | `ae43373551530b62` |
| I-121 | `incident-uq` | 72 | да | — | `0d9d3be73cc10602` |
| I-122 | `incident` | 71 | да | 73 | `fac91edc80fd07bc` |
| I-122 | `incident-uq` | 72 | да | — | `1839b55d85c05039` |
| I-123 | `incident` | 71 | да | 73 | `9bf4c4b2c4b63e21` |
| I-124 | `incident` | 73 | да | 71 | `86d4ab0ed67f3e33` |
| I-125 | `incident` | 73 | да | 71 | `0342ca2f042be52d` |
| I-126 | `incident` | 75 | да | 76 | `c4aac49ce48ddfbb` |
| I-126 | `incident-uq` | 76 | да | — | `1ebe2e7b6c5779c0` |
| I-127 | `incident` | 75 | да | 76 | `b0ff25a5585dc74c` |
| I-127 | `incident-uq` | 76 | да | 56, 64 | `d49f79fa15a26c1f` |
| I-128 | `incident` | 77 | да | 19, 23 | `182d793fa2d713b4` |
| I-129 | `incident` | 77 | да | — | `d7e3a4939414b378` |
| I-130 | `incident` | 77 | да | — | `548297ded9eb760d` |
| I-131 | `incident` | 77 | да | — | `7051fbb3cc52ffa9` |
| I-132 | `incident` | 77 | да | — | `a8ca22e244e276ee` |
| I-133 | `incident` | 77 | да | — | `ccaba2a1d87674e5` |
| I-134 | `incident` | 77 | да | — | `a658a5b67d7e20a5` |
| I-134 | `incident-uq` | 78 | да | — | `7b541aa7cc85edd3` |
| I-135 | `incident` | 79 | да | 80 | `b21b64eeae1b7b03` |
| I-135 | `incident-uq` | 80 | да | — | `aff362677d969808` |
| I-136 | `incident` | 79 | да | — | `0c0a8b4339abb280` |
| I-137 | `incident` | 79 | да | — | `5d8f37061697ba51` |
| I-138 | `incident` | 79 | да | — | `5ed29b009c24fabe` |
| I-139 | `incident` | 81 | да | — | `e02da91576f28145` |
| I-140 | `incident` | 83 | да | — | `a1088e1d29e10228` |
| I-140 | `incident-uq` | 84 | да | — | `bbf089b86fe08aa9` |
| I-141 | `incident` | 85 | да | — | `729dc9d3fc61eaf3` |
| I-142 | `incident` | 85 | да | — | `81a82478a9c8bfc2` |
| I-143 | `incident` | 87 | да | — | `a90798b6da218022` |
| I-144 | `incident` | 91 | да | — | `1a80ed9ea0ff9e47` |
| I-145 | `incident` | 91 | да | — | `2ecf0d9d027bf194` |
| I-146 | `incident` | 91 | да | — | `d091b2aa484bc531` |
| I-147 | `incident` | 93 | да | — | `168ccbaed024821b` |
| I-148 | `incident` | 93 | да | — | `cf7c84193b41ddb1` |
| I-149 | `incident` | 93 | да | — | `01af8288b0b25ba9` |
| I-150 | `incident` | 93 | да | — | `1885b2932073917c` |
| I-150 | `incident-uq` | 94 | да | — | `641edd4bbe2975a4` |
| I-151 | `incident` | 99 | да | — | `4782417344df8033` |
| I-152 | `incident` | 99 | да | — | `a2ab6d627d1e8f1d` |
| I-153 | `incident` | 101 | да | 75, 77, 79, 86, 87, 88, 89, 99, 100, 108, 116 | `311bfc07f6ac4709` |
| I-153 | `incident-uq` | 102 | да | — | `77e069b87553684a` |
| I-154 | `incident` | 103 | да | 99, 100, 101 | `f4fc76a3fa926d09` |
| I-155 | `incident` | 105 | да | — | `e9c083f223c0bd15` |
| I-156 | `incident` | 105 | да | — | `158f71aa72ffdac9` |
| I-157 | `incident` | 105 | да | — | `75ef9b55e5c1bb25` |
| I-158 | `incident` | 107 | да | — | `8f9cd95bb172f3f7` |
| I-159 | `incident` | 107 | да | 58, 63, 64, 65, 67, 79, 89, 108, 116 | `3fe58a85419fc15f` |
| I-160 | `incident` | 111 | да | — | `48b94182ccc50d21` |
| I-161 | `incident` | 111 | да | 113 | `58a6d75da2348ff8` |
| I-162 | `incident` | 111 | да | — | `3e47683069903ae5` |
| I-163 | `incident` | 111 | да | — | `152b8837760e0f04` |
| I-164 | `incident` | 113 | да | — | `4716e9c2cc1afa0f` |
| I-165 | `incident` | 113 | да | — | `c7ae72805680c486` |
| I-166 | `incident` | 113 | да | — | `c30603de4334c607` |
| I-167 | `incident` | 115 | да | — | `9a633e25d7510e1b` |
| I-168 | `incident` | 117 | да | — | `97fb57e5e238a98d` |
| N-01 | `negative` | 9 | да | — | `fd1294447b3b12cf` |
| N-02 | `negative` | 51 | да | 7, 43, 93 | `5dd35fd0395b4daf` |
| N-03 | `negative` | 65 | да | 53, 55, 57, 58, 59, 63, 64, 67, 108, 116 | `fee9a2fbeb0d18d1` |
| N-04 | `negative` | 89 | да | — | `e0aeab794a6f5c3c` |
| N-05 | `negative` | 89 | да | — | `73b445c3539aabbe` |
| N-06 | `negative` | 97 | да | 7, 39, 45, 99, 116 | `311d00c42821fd34` |
| N-06 | `negative-uq` | 116 | да | 7, 45, 97, 99 | `2f4deadbe2b45d62` |
| N-07 | `negative` | 101 | да | — | `96934157d1eb19b4` |
| N-08 | `negative` | 107 | да | 47 | `a6bed16b0046de6d` |
| N-08 | `negative-uq` | 116 | да | 107, 109 | `64552e2a29474b13` |
| N-09 | `negative` | 117 | да | 116 | `0eb9120475ee70cc` |
| SC-01 | `success` | 8 | да | — | `c468a14dbeca7686` |
| SC-02 | `success` | 42 | да | — | `e6b91f64cfd35b61` |
| SC-03 | `success` | 42 | да | — | `8b749f50280b0ba6` |
| SC-04 | `success` | 46 | да | — | `5a97a6c18730d827` |
| SC-05 | `success` | 26 | да | — | `9ebc64af444a9772` |
| SC-06 | `success` | 48 | да | — | `5eb4ee96f0ef751e` |
| SC-07 | `success` | 50 | да | — | `f496f422509a3056` |
| SC-08 | `success` | 52 | да | — | `e9c813f0cf777757` |
| SC-09 | `success` | 58 | да | — | `583f4820058ea228` |
| SC-10 | `success` | 64 | да | — | `755b5a708eee6b9d` |
| SC-11 | `success` | 66 | да | — | `c37d1a37057c497c` |
| SC-12 | `success` | 72 | да | — | `1839b55d85c05039` |
| SC-13 | `success` | 76 | да | — | `dc654e117427e602` |
| SC-14 | `success` | 80 | да | — | `aff362677d969808` |
| SC-15 | `success` | 116 | да | 86, 88, 89, 108 | `dafd61effa0e5abe` |
| SC-16 | `success` | 116 | да | 86, 87, 88, 89, 108 | `674ab5f034f314c9` |
| SC-17 | `success` | 116 | да | 108 | `d819ee7e139e6a7c` |
| SC-18 | `success` | 116 | да | 79, 86, 87, 88, 89, 108 | `6c05630247b17826` |
| SC-19 | `success` | 116 | да | 79, 86, 87, 88, 89, 108 | `a4052937568aa888` |
| SC-20 | `success` | 116 | да | 97, 99 | `eda225f25e06c369` |
| SC-21 | `success` | 116 | да | — | `b7d48a85ef1da988` |
| SC-22 | `success` | 116 | да | — | `311cff7cdb9ad53c` |
