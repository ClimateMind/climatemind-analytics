/*
Owner      : Andrew Banister
Created On : 2021-07-04
Notes      : Run this script and use the queries labeled near the end to populate the Climate Mind Feed Engagement dashboard.
*/

-- these should be permanent tables in the analytics schema
CREATE TABLE #dev_session_uuids (session_uuid VARCHAR(50), test_removal_process VARCHAR(50));

INSERT INTO #dev_session_uuids (session_uuid, test_removal_process)
VALUES
('0e22e0ee-9946-4e61-b35d-ed6b02d7672b', 'top_left_cluster'),
('ca3b78e1-8e0f-4819-8c38-9afdd5ea13d1', 'top_left_cluster'),
('6add2898-9d6b-4aab-bb1b-f5527bd8f4d1', 'top_left_cluster'),
('13df12fc-aee6-484a-b344-0fe3c4ad6a96', 'top_left_cluster'),
('f5fca425-1332-42f6-945c-38fff494a438', 'top_left_cluster'),
('45dab855-9685-4d62-a5f8-90b5b1c72965', 'top_left_cluster'),
('50311d72-e4be-4825-b9a0-7fc8e21ebd32', 'top_left_cluster'),
('cb6c4d72-17ee-4ca5-9505-ea357ccd91e6', 'top_left_cluster'),
('244e0cab-80b4-4309-be75-0c7ce4a31633', 'top_left_cluster'),
('cb01c86d-6214-4b75-8ff2-218d3188972b', 'top_left_cluster'),
('b93149ee-3820-431c-b6b7-1ceecee0d448', 'top_left_cluster'),
('34093d2e-37fc-4fb2-bdd7-c0008d467160', 'top_left_cluster'),
('9c2fc617-e549-4426-841f-bdcc63386db9', 'top_left_cluster'),
('d0fa16c0-ebeb-4bdb-80d6-3ee2c0e15551', 'top_left_cluster'),
('86006d84-633f-472a-a562-30672b49efd1', 'top_left_cluster'),
('9057d4d0-93b4-47a0-b2dd-1abf94512b79', 'top_left_cluster'),
('95fd582f-1801-431a-a13b-4c5d2762d102', 'top_left_cluster'),
('4ae903ad-1ed4-4257-8953-83ba90b3c405', 'top_left_cluster'),
('aeb9f0f8-ba58-474c-bc1f-6bb1d0789e91', 'top_left_cluster'),
('51195e17-628b-4ce5-b73d-df6b79b4d894', 'top_left_cluster'),
('debf8057-5fc7-4770-8c2b-91dd7c723082', 'top_left_cluster'),
('487b7f0a-5b49-44de-a116-9160928bd4a0', 'top_left_cluster'),
('435222cf-15cf-496f-8d78-980e26422d77', 'top_left_cluster'),
('126ac165-5e1a-45a4-9aae-d038e6c8cc69', 'top_left_cluster'),
('4912610b-a25e-4d84-9db1-26ed78869295', 'top_left_cluster'),
('c0e3c03a-5dde-4e20-a3ae-7c8dd6e76848', 'top_left_cluster'),
('56703a25-47e5-4202-9477-2cbc7e2080a3', 'top_left_cluster'),
('d42698a8-71c4-4624-8a2b-ebe19b9f8f17', 'top_left_cluster'),
('3a8cca6a-fa54-4230-85f3-7e0ba1fb57e3', 'top_left_cluster'),
('38de334a-0415-4b2e-a388-7dee52a3be09', 'top_left_cluster'),
('1e11e716-69d3-4be5-b1ea-be38a57d7bcc', 'top_left_cluster'),
('5c35b42a-136d-4458-b16d-9a9a745d136c', 'top_left_cluster'),
('af1a563a-39e0-496b-b8bf-287527a0f609', 'top_left_cluster'),
('0d7febcb-670b-4d63-a640-c83ffd272a60', 'top_left_cluster'),
('436d266f-4ad7-48d5-96c5-a42059499eb1', 'top_left_cluster'),
('5f2af124-f073-44f1-bf16-7aa49f5d9b6c', 'top_left_cluster'),
('c3acb656-b70c-489e-bf36-65b0f9413876', 'top_left_cluster'),
('d282f440-983a-4d3a-8d5f-63e86d6685b5', 'top_left_cluster'),
('f5525156-1afb-4235-bb1c-3ea05de41a94', 'top_left_cluster'),
('3c586a52-e831-4b7e-9f6c-54c61897af8c', 'top_left_cluster'),
('4898fd24-2c6f-4672-88b7-25521d05ef43', 'top_left_cluster'),
('939b1b06-f58d-400d-8ee4-d673447c7f22', 'top_left_cluster'),
('e49d0d7a-e0de-4520-8d51-9eee2807adbc', 'top_left_cluster'),
('29e8d677-65fe-4e69-956c-0e8b7b980bad', 'top_left_cluster'),
('fba5fcd7-31b2-452f-a17a-2f9a6086bfe0', 'top_left_cluster'),
('ad5684ab-3b27-4a8b-9d7f-29d2b302d260', 'top_left_cluster'),
('f2532c3d-4196-4760-b183-da423aeb7d44', 'top_left_cluster'),
('88e3ead4-9b7d-464e-b3cf-0ed7ac84dbb3', 'top_left_cluster'),
('eedcdfb1-32ba-40ad-9096-3f52bd65eada', 'top_left_cluster'),
('0b8b8c29-ae84-43d5-b56f-91e5c6b52a7d', 'top_left_cluster'),
('efe4f6f8-68a2-4c35-bf87-f90de72797c3', 'top_left_cluster'),
('6a62f2e2-d687-45cb-b238-4753e0dc3935', 'top_left_cluster'),
('ec31014f-9475-4967-b88c-6e34bf13c7b2', 'top_left_cluster'),
('062bea10-04b3-4fe3-852e-b5bf7b4c0da3', 'top_left_cluster'),
('43b8b8b7-cd3a-4344-830e-1cf4411895ed', 'top_left_cluster'),
('713cb48b-ab1b-47b8-b432-dfde4fb5fd3f', 'top_left_cluster'),
('64f0caca-5578-400d-84e4-567123d3c562', 'top_left_cluster'),
('9fd7d020-47c8-4bd6-8b40-97f192c09503', 'top_left_cluster'),
('e88cafbf-a685-4347-96b9-7f936fca239f', 'top_left_cluster'),
('3591d2f6-af29-4509-bb6c-3776f914cfd2', 'top_left_cluster'),
('57f04a8e-46d5-4337-9ceb-6dbaf8749349', 'top_left_cluster'),
('6d4dcf29-e7d1-4c3a-92f4-8343f2b18c9c', 'top_left_cluster'),
('98313933-9b47-49a6-aefc-5ebbdc6b9c6f', 'top_left_cluster'),
('e95bdef9-9673-45ee-b15b-662b63fe3f52', 'top_left_cluster'),
('2b4ec433-15d8-4370-8af4-e650ac7cdb2a', 'top_left_cluster'),
('0ef02c56-bb36-46cb-845e-47f1a7f90fec', 'top_left_cluster'),
('6326e4c1-64f6-40fa-a39a-05928e3f88ea', 'top_left_cluster'),
('8198c095-5ca1-4ad0-ae77-cdcc288b1c43', 'top_left_cluster'),
('c5d980c4-3c92-429f-9d35-54bef2497e3f', 'top_left_cluster'),
('0099fdb9-b36e-4372-b7fa-6cc42f75ad7a', 'top_left_cluster'),
('8617e81d-06ff-4d9c-811e-459f0dfa0ef9', 'top_left_cluster'),
('fa59d81d-cdb0-43ec-bc0c-4fe4275161d4', 'top_left_cluster'),
('ef145667-5013-48a4-b46f-bf9c426b5bbb', 'top_left_cluster'),
('99b01a05-c696-458b-8fe5-55370a4ae81b', 'top_left_cluster'),
('b052944a-3d03-418e-92f3-4dc866ded377', 'top_left_cluster'),
('da5e6e3c-e524-44ff-8ac3-0e4883ae6ab6', 'top_left_cluster'),
('5c5a3990-289e-417f-82de-2a86344ff149', 'top_left_cluster'),
('5fb85b53-d421-45f5-9006-e28b4737c205', 'top_left_cluster'),
('ac4cafa9-03d9-4fd5-929e-12c7fc9c71e2', 'top_left_cluster'),
('911aee52-e22c-4561-bc8f-4827867578d9', 'top_left_cluster'),
('2b9beb40-c814-40ec-b9b6-554a60b15e09', 'top_left_cluster'),
('3bc73845-0aa3-483b-8a0b-f7cb1cd23ffa', 'top_left_cluster'),
('33d75033-de0c-452c-b8fc-9a36c88f305a', 'top_left_cluster'),
('a72b4f9f-8ab5-451f-8518-32bb2819161d', 'top_left_cluster'),
('df28ceba-7276-4ba2-8f5f-fa99275d2f7a', 'top_left_cluster'),
('3338977c-fb7a-409a-9370-fbd52502ef13', 'top_left_cluster'),
('40820a28-f543-467e-9600-ba75fe8878a9', 'top_left_cluster'),
('8df54a78-83d4-49d2-900f-6526e689e8aa', 'top_left_cluster'),
('ffc6b260-c4e2-4c73-bb71-e53ecb135c8c', 'top_left_cluster'),
('ef5f82e5-37aa-490c-b766-37e6d36b7e26', 'top_left_cluster'),
('b543fc06-0543-4dbe-947b-4074fb2bcefd', 'top_left_cluster'),
('29257fdd-ed7d-4395-877a-768b3364ef1f', 'top_left_cluster'),
('13ceacfa-976c-46bd-848d-da44a77fb779', 'top_left_cluster'),
('c13b45ee-eb57-41a3-93a3-dc2269f3ba12', 'top_left_cluster'),
('5585fcc7-2203-4539-b7fc-5169e3412c02', 'top_left_cluster'),
('c8651ebb-9368-42be-a6c7-ae088e63ed19', 'top_left_cluster'),
('35f8a29a-b245-4a34-889a-b4616f2aaa01', 'top_left_cluster'),
('5f8270a5-4404-4adc-81a1-d15da50d8ece', 'top_left_cluster'),
('da2e5b52-b8e9-4e69-927b-0aa4f83153d4', 'top_left_cluster'),
('3c12e9f0-9b5c-48ea-9c7e-e7fd4d17aad9', 'top_left_cluster'),
('5c343296-59f8-46ef-8fa5-ce7bc0f7b20c', 'top_left_cluster'),
('2d137461-3ff7-471f-b194-39cc76f70e2b', 'top_left_cluster'),
('80df679a-855e-4a44-a37a-4695dd34462f', 'top_left_cluster'),
('3512e536-1dee-4ada-bb53-7869e4da91f4', 'top_left_cluster'),
('d08d218b-a263-44cd-a19a-fdc8a06f8e04', 'top_left_cluster'),
('ba622b86-8a0d-4d1f-9ba6-1f740a3bfc06', 'top_left_cluster'),
('010f443a-e5e5-4477-9b34-22ef004ebd62', 'top_left_cluster'),
('eb9d8dd6-fdf8-45da-9722-c2ee56e7687f', 'top_left_cluster'),
('652ebbbf-3a92-4f4d-8cae-75eb3e79e93a', 'top_left_cluster'),
('5963e7ed-ea19-4929-a4ad-c2821c268060', 'top_left_cluster'),
('9c0929a1-750d-4d3a-922a-b7a2f94daef0', 'top_left_cluster'),
('348e35a0-6eae-4b83-a52c-3a116638fc8b', 'top_left_cluster'),
('a7351949-aed1-47f1-9ac8-3f1189a5039d', 'top_left_cluster'),
('b7a3b5f5-2b50-471a-bb20-12420cd7c645', 'top_left_cluster'),
('7316e097-5ab2-4aae-87f9-452c2ff7dfad', 'top_left_cluster'),
('ceedea77-8705-4410-90b5-8dcc3086b254', 'top_left_cluster'),
('8717b3bb-03c2-4a5c-95fe-7855cac93d4b', 'top_left_cluster'),
('b264cfd5-4adf-47c1-862b-fee7945bd759', 'top_left_cluster'),
('1fd06cb0-eb5d-44be-87ba-05f9ebaca756', 'top_left_cluster'),
('4deeda39-5435-4f82-94b4-735cde233bc6', 'top_left_cluster'),
('a2485596-fb3f-48a9-9f20-81581da67e58', 'top_left_cluster'),
('dd2a0d71-4430-4cfd-969e-668a47f1e322', 'right_cluster'),
('e07ef161-4b4c-430a-8617-5e4852d213dc', 'right_cluster'),
('0e3990e7-7508-41a9-bed8-5f0207abe874', 'right_cluster'),
('d4af3c98-6897-4e84-aa82-41ff5c6e80d9', 'right_cluster'),
('e61a35b3-741c-4dcc-b515-0a662c145374', 'right_cluster'),
('28b49b15-0d41-4e90-93e2-3c8516bfddbc', 'right_cluster'),
('0dc23bfa-5cca-435a-919e-ba801accfe2a', 'right_cluster'),
('dcaf8f10-f096-42c4-860c-3690e130bc47', 'right_cluster'),
('0f7d5e45-2758-435a-b44c-61ee088f940f', 'right_cluster'),
('400b53c7-0541-41d3-9022-c4521ca2f861', 'right_cluster'),
('67dc5420-3b52-482b-8182-f828575d3c1f', 'right_cluster'),
('d1c0562d-a050-46d4-a5f3-c63a1bc5321e', 'right_cluster'),
('773f6c0e-fde2-4f33-9288-a3748aedda59', 'right_cluster'),
('c2b6e04f-7f91-443c-b09c-c652c7cdb9af', 'right_cluster'),
('b64f3bc5-2c73-4dc4-932f-b146ddf2f28d', 'right_cluster'),
('e1f4d7f8-e774-4663-ad8c-e90d000cca4e', 'right_cluster'),
('c571a797-1810-463e-b7f3-f9d942fbe9b4', 'right_cluster'),
('460b76b0-d9ce-4c8d-9c1a-8711a859f55f', 'right_cluster'),
('ecda5259-ff56-4b98-a628-219c7b7b0c5f', 'right_cluster'),
('d18ef956-bfdc-4472-8ec1-fbb3720f3b7e', 'right_cluster'),
('a05b76a9-1c63-480f-8fb1-6634c7b2d8dd', 'right_cluster'),
('4f3eb3d5-f249-4e38-b38d-8dbe72352d21', 'right_cluster'),
('92b9a0f3-6b89-4850-bffc-d0ef0275f837', 'right_cluster'),
('b3ba6e9c-4e85-4c72-8472-9c241534981e', 'right_cluster'),
('89a4873b-ae85-4236-a6cc-1ae7a1023e39', 'right_cluster'),
('b1d36c29-8acf-420f-ba75-aa34ea930dd8', 'right_cluster'),
('ae2938b3-a4e3-4cd3-a323-87fc65dd96ff', 'right_cluster'),
('86c0f487-8395-4107-8814-b6274ec0f3f5', 'right_cluster'),
('c9e65e8b-14f4-4ace-8928-584f792830bd', 'right_cluster'),
('c19c714d-3a89-46e1-9136-4acc5ca9f292', 'right_cluster'),
('95feb5e9-51c4-45ba-9b1d-deaa3557cfc7', 'right_cluster'),
('3768dbe0-2845-4ef6-aef2-1fe682644e65', 'right_cluster'),
('387ad532-dd34-4521-af10-c6e7ce3fe938', 'right_cluster'),
('03f310c2-26ad-47a8-9f1a-485cff25754f', 'right_cluster'),
('e1bc1295-ba77-4fa1-9988-a87ec83f537c', 'right_cluster'),
('c7baa4f9-bc81-42b4-aef6-ae7c4a5943a8', 'right_cluster'),
('40722733-1675-4abf-9483-68500e2d77d3', 'right_cluster'),
('9e7d3cce-7b27-47cd-befe-d11580c6c4bd', 'right_cluster'),
('efc4b739-3576-47c6-b3f4-bff2f6ca9f03', 'right_cluster'),
('347d7cab-6cc4-4a0c-9a0f-a9f466c5cd9c', 'right_cluster'),
('fb2d366b-6641-4495-b3d2-4d840533defe', 'right_cluster'),
('90622bc2-d54c-485e-a782-88512754b3fc', 'right_cluster'),
('a2cc3bff-4a86-41a6-abc3-77307d3669aa', 'right_cluster'),
('389fca0b-2bf2-4543-8acc-a4b8528ea0c2', 'right_cluster'),
('37b8f848-9fba-4517-a88e-ad2dc3371612', 'right_cluster'),
('acdb4cac-42b5-4edd-b0b2-539d9f2a17b4', 'right_cluster'),
('7c4ffb31-5a90-4a10-979d-84badc584566', 'right_cluster'),
('bd54a6cd-76b8-416f-8000-f418c9009683', 'right_cluster'),
('2c5039b9-cd72-4eca-8d9b-e9f8f154238e', 'right_cluster'),
('eff9cd70-ec1b-46b3-a854-db3d464fa890', 'right_cluster'),
('5a3b0a5c-f432-4b53-8e98-9c23262ce86c', 'right_cluster'),
('876e67bf-e4b3-4850-9d09-92b98e24ff30', 'right_cluster'),
('b8f18d27-af87-4b82-b0b2-b34875adc16b', 'right_cluster'),
('181b5530-8da9-4254-951e-c7bd6ab839c6', 'right_cluster'),
('1196d82d-b708-43ee-b321-09611e2f7a63', 'right_cluster'),
('60bb8990-9d0c-43c0-869d-b66261588d2a', 'right_cluster'),
('e495c617-1b70-40ff-8acc-74316e2a121a', 'right_cluster'),
('99db24ae-97fd-4d99-8827-f17c5dea811b', 'right_cluster'),
('3767fdba-af3e-47cc-8e03-6a6b816c866c', 'right_cluster'),
('6da86f74-43b0-43e6-b12a-afb4495f6b2d', 'right_cluster'),
('8ff89b6b-5039-44a1-977b-03611b873237', 'right_cluster'),
('7bdfa58b-d380-433c-87ff-615b67eae918', 'bottom_cluster'),
('0df80b5d-d5b3-4703-a35b-02736cd7ec9b', 'bottom_cluster'),
('4a1755f5-336e-4c28-86af-7e8a5e819674', 'bottom_cluster'),
('9cfdf5f4-7190-4860-830f-f18a229a80fb', 'bottom_cluster'),
('4e187bfe-688b-4dc0-a695-720fe7e54253', 'bottom_cluster'),
('c2f0d29d-1bfb-4619-ad1d-f9e216b20fca', 'bottom_cluster'),
('6b1196bb-55ca-4a1b-8349-3d24a2684eab', 'bottom_cluster'),
('dfd5b5b9-f6d5-429a-8a6e-caa07ecc0b9a', 'bottom_cluster'),
('c7e89aba-8a9f-4a09-abcb-3baa87dd3e23', 'bottom_cluster'),
('08627f66-0e6e-46d4-94dd-fc478e20095e', 'bottom_cluster'),
('1d896b8c-ab07-45e7-a1ef-33e5bb4cb9fb', 'bottom_cluster'),
('a18d5f45-49e1-4de0-ba33-ef24b4c6745d', 'bottom_cluster'),
('1a30b1cc-ad6b-4d20-9f74-9241c32c5598', 'bottom_cluster'),
('f5337e71-1ce4-4dc7-855f-fc64137318f4', 'bottom_cluster'),
('3c581e6e-3977-4ef3-ae53-1f060d4a7a61', 'bottom_cluster'),
('b5042079-20f2-4f44-a928-32c54d33f8ac', 'bottom_cluster'),
('9df37c50-07e2-4417-a7f3-9071c0d56bd7', 'bottom_cluster'),
('8413030d-6802-428c-82fc-c8fbc3cccf04', 'bottom_cluster'),
('46b1737f-f7fb-4605-a0ec-444c87c5de78', 'bottom_cluster'),
('b802789b-f2c1-49e5-8077-751b3875854c', 'bottom_cluster'),
('fa5a1afa-d93d-40d8-bc33-cca978f5665c', 'bottom_cluster'),
('3af3c35d-bece-4e4a-901d-7446a0bf1233', 'bottom_cluster'),
('a18f3d98-c02a-4c78-8092-78227559ee64', 'bottom_cluster'),
('409263af-1c97-4af6-b9df-7099602cde1a', 'bottom_cluster'),
('eb95b91b-4185-46d2-8327-51176412da0f', 'bottom_cluster'),
('f861cd21-ee00-4440-becf-ef5c4af60f0e', 'Yasmine'),
('381ca618-8721-4794-80eb-659e9e86960e', 'Yasmine'),
('a422335e-a55b-4658-b97e-3bb5c8dfc067', 'Yasmine'),
('add5812a-f094-44f2-a0e8-114fc94bd758', 'Yasmine'),
('3a16556b-385f-442c-b4cf-6b471c4b87b8', 'Yasmine'),
('7cbd13b3-d13c-4008-becb-145d4963bffa', 'Yasmine'),
('50afd32f-07f7-4ae5-a453-bd2fd1d53519', 'Yasmine'),
('9a411bdc-d76a-4055-b1b1-87db3daff733', 'Yasmine'),
('994ce8f7-0fcf-4e31-9f1e-ef30bdebb2ff', 'Yasmine'),
('a9f47cec-20ad-4752-ae73-92ba61ac304c', 'Yasmine'),
('e41bd9b2-77e9-4791-ba0c-048e8d82d199', 'Yasmine'),
('40013a02-763d-4537-b4a7-d31ac8db42d6', 'Yasmine'),
('2fca2f8f-6d0c-4ec6-b0e6-dbc1dc53cd95', 'Yasmine'),
('b998365e-ea9b-411a-ad2f-e0d138ba4032', 'Yasmine'),
('96ee9a2a-39f7-41ed-a282-51bda97969d5', 'Yasmine'),
('77b25ac0-496d-41cf-b810-5cf189b169f8', 'Yasmine'),
('e02accba-fda8-4d82-8757-d3054926ef2b', 'Yasmine'),
('91e91615-9ea9-43e8-bc71-377ec6954b64', 'Yasmine'),
('5e692987-a842-4587-9852-f8587fccf2db', 'Yasmine'),
('c611e633-c796-4bd3-8bdc-84a60a8f4159', 'Yasmine'),
('b4f8e320-2480-4e4c-b04f-ee94955bfa35', 'Yasmine'),
('b3995968-0115-43c4-a4da-bd57599a49aa', 'Yasmine'),
('a705ae5c-4660-406b-84a7-b9cffe0c18c0', 'Yasmine'),
('a85e1f0b-ef68-4b3c-a308-8efd2d152d40', 'Yasmine'),
('619496dd-d683-4eda-928c-4eb7fc327754', 'Yasmine'),
('bfa0cb5f-d97e-40af-bafe-dcc487ffa188', 'Yasmine'),
('667d7eab-39b3-43ed-b7a8-bcbaa973cd86', 'Yasmine'),
('94578a74-9103-46c9-8c9a-71fa7599f13a', 'Yasmine'),
('913f8017-bf90-490f-9917-538ce58f8432', 'Yasmine'),
('c2c6f8c7-1606-4b16-b0b9-adceb7eda946', 'Yasmine'),
('265e162d-bd6f-4415-a5d3-007cfa3a4594', 'Yasmine'),
('c64b1c3e-133e-430c-969c-b6e22c9b88c7', 'Yasmine'),
('ba2b9993-3499-4a5f-a4db-118a50146e72', 'Yasmine'),
('f704e87c-6668-4660-b758-38b69f94bd8b', 'Yasmine'),
('548ac839-bada-4269-bd0d-094e09c391fc', 'Yasmine'),
('25f07c5b-2973-40f3-ad50-7cd654f3fb86', 'Yasmine'),
('79ed6a68-5080-4622-8f53-07b06bc09bc0', 'Yasmine'),
('a057756e-5f25-4960-a0f2-b94ceddea02e', 'Yasmine'),
('a039bb0a-e716-4b45-841f-b16fcf428e45', 'Yasmine'),
('c81efd2d-a74e-42b9-aacd-f3b23e339695', 'Yasmine'),
('afdcaa2e-0183-4097-bce1-b40f08eb6007', 'Yasmine'),
('c88c570c-6de7-4a7f-b7f5-9257d52a28b7', 'Yasmine'),
('6dcdf634-294f-402a-83b3-5194c3635fb0', 'Yasmine'),
('15c69899-6505-4a98-877e-ae42e5b81856', 'Yasmine'),
('c10c9ffa-dd15-49c0-81c6-7debdac5ce5a', 'Yasmine'),
('47053722-75be-4a5d-b551-1e5cd1ca7ea3', 'Yasmine'),
('e2b51f45-ab2b-4469-978b-00e374f4994b', 'Yasmine'),
('94fa5490-98a2-4be1-abf8-10191e2a0cdd', 'Yasmine'),
('11045fff-4569-4a35-a87c-7435e5309172', 'Yasmine'),
('de2296fa-44da-4572-a1e8-43494d64013e', 'Yasmine'),
('5a771c2a-2bc9-42c6-a170-1b88d3512019', 'Yasmine'),
('fd573205-7cd5-4628-a20e-a16ba7a657aa', 'Yasmine'),
('579359ff-55f5-4ab8-a7bb-7155c2c6de4c', 'Yasmine'),
('586df415-d2c1-4b63-8703-bb1b8b6273d2', 'Yasmine'),
('e80d27d2-7fc2-4926-a841-6fff2fe5c2af', 'Yasmine'),
('4fbae457-0dc1-4854-8d60-df0be7bdaacb', 'Yasmine'),
('7ddd3afe-14e1-4c05-a37d-c4c9b4d6bece', 'Yasmine'),
('4914fba4-afdc-4a41-9201-9624d324df79', 'Yasmine'),
('485815dd-6071-49ba-aff5-8a840d821a54', 'Yasmine'),
('390d1e3e-c8e1-4d9d-af49-90a4b005f98c', 'Yasmine'),
('8fe1fc28-d4e2-461b-868a-2439225e50c5', 'Yasmine'),
('a5fcfa9d-e0bd-45be-a945-309fcc9605fb', 'Yasmine'),
('318d4ed0-eb3e-4959-bdff-3f1a1faa5f8b', 'Yasmine'),
('6f3f3fcd-8fc9-469c-aa64-d337273abd07', 'Yasmine'),
('02160019-d8d8-494f-b6a9-05eb8d9d2732', 'Yasmine'),
('4ee8e737-1f6e-4cad-934c-8417bde9863c', 'Yasmine'),
('26e5964d-6778-416d-a8d2-4a72854d9dc4', 'Yasmine'),
('257c36a0-ef79-42a7-839d-3d3000ef0120', 'Yasmine'),
('860547b8-9be3-4d84-b56b-62bae89e06fd', 'Yasmine'),
('4a3d330f-0a87-4e35-a968-bc4218a27dae', 'Yasmine'),
('29b0fce9-4e8b-4ccc-9ea7-ce3329971432', 'Yasmine'),
('128c5d3a-baf6-47ad-9aaf-48420490cac5', 'Yasmine'),
('ac964f84-628e-4242-9199-5a29db27cb43', 'Yasmine'),
('58a26e4e-2f4c-4f70-913a-13a55f1a024a', 'Yasmine'),
('66caf84b-6243-4127-8a69-671901ae5a10', 'Yasmine'),
('a76793a9-2951-4570-8d8a-c7666afe7bc6', 'Yasmine'),
('e991f6d2-97e4-447e-a74c-eacd0322bf32', 'Yasmine')
;

CREATE TABLE #climate_mind_nodes (card_iri VARCHAR(50), type VARCHAR(50), label VARCHAR(250));

INSERT INTO #climate_mind_nodes (card_iri, type, label)
VALUES
('R9GgwNAE1EIyeCTZohpIThL', 'effect',  'political polarization'),
('R5eVKPmEff8f7D8VBAEEC8',  'effect',  'more heat absorbed by land'),
('R8vDHwP7soRN6c6XWYDjJkH', 'effect',  'more heat absorbed by oceans'),
('RoGet2DtXzFfCBQSjgRW3z',  'effect',  'more heat absorbed by ice'),
('Rtzkdtty1BHKfI8whB6qWR',  'effect',  'more heat absorbed by air'),
('RndlLhwHuWP9Ng5SgdZij3',  'effect',  'warmer air and atmosphere (tropospheric warming)'),
('R7yY9aSXNoealJHEP1iluxl', 'effect',  'decrease in frequency of cold days and nights'),
('R7zeFSAP7x3PT5rG0i1BLVe', 'effect',  'increase in evaporation'),
('R9vkBr0EApzeMGfa0rJGo9G', 'effect',  'increase in toxic air pollutants (air pollution)'),
('RBAJ46soLY6Nmd73XuHajVc', 'effect',  'more moisture (water vapor) able to accumulate in air'),
('RDudF9SBo28CKqKpRN9poYL', 'effect',  'increase in frequency of warm days and nights'),
('RJAL6Zu9F3EHB35HCs3cYD',  'effect',  'increase in frequency of heatwaves'),
('R7Yo5FYFleUwkbXjCU3xo4E', 'effect',  'decrease in test scores'),
('R7pS7MtLuEDp8HhEyf1VtOE', 'effect',  'increase in health costs'),
('R8epBa4UvcieLTynfK3E84u', 'effect',  'decrease in population of moose available to hunt'),
('R8t0oNsG3WgnupXsBVSjMHZ', 'effect',  'increase in suicide'),
('RBqibfoxaYmRDDRiBzSVS0N', 'effect',  'increase in heat stroke'),
('RBvy0CVizhdMfXbtJIc2En',  'effect',  'decrease in GDP'),
('RDfWjsojED1JhyonjjYn5T1', 'effect',  'increase in worker absenteeism'),
('RpOmwCPDUgT3EfGsy4qV4B',  'effect',  'increase in temperature of work environment'),
('RzalB19SQSGGVxprHL33Ik',  'effect',  'increase in risk of heart attack'),
('R8VWiAcECOGFY5bloP4988I', 'effect',  'increase in death'),
('RDuEdzMOhOt76COW2RVxZdP', 'effect',  'decrease in worker productivity'),
('R53XvTdJg0OnBAgtt0ldAm',  'effect',  'increase in ground-level ozone'),
('R8Fa34SNdEwdj93hXO0oMS',  'effect',  'decrease in learning (without air conditioner)'),
('RDavliTi6W93xwahwtUnUtG', 'effect',  'increase in physical violence'),
('RtcWDD6Pcr6vIrMhOObmOE',  'effect',  'increase in sexual violence'),
('R1d2BVvduMHLTUVxQ9qdpd',  'effect',  'increase in extreme precipitation'),
('RscUzlKgdFQVS80E8cOyQZ',  'effect',  'increase in H2O vapor'),
('RnbPKhyIQNnShkRKHqGrGm',  'effect',  'increase in flooding of land and property'),
('R8uV2oTMZHslQ6qiGWJ8OQO', 'effect',  'increase in destruction to US military bases'),
('R8xnqMTv1FH2zTsQT4ckrRi', 'effect',  'increase in cholera infections'),
('R90voMtk6xBMoARwvKc2wuy', 'effect',  'increase in climate refugees'),
('R9ah7PByb0OgSOa90WQQdjc', 'effect',  'increase in deforestation'),
('RBJi2ztbJiaIwcTQTScEKNx', 'effect',  'increase in CO2'),
('RDAmSaOOexqzo8f9kE5JXMR', 'effect',  'increase in erosion'),
('RCpXSHQAIxJpX4uyqhk82TF', 'effect',  'increase in river flooding'),
('R5kluaMVlhzpGZEWgAsy1',   'effect',  'more acidic oceans (increased dissolved CO2)'),
('RC9SyXE5PhiT6iKz1LaJFgf', 'effect',  'negative effects on cognition'),
('RDz5mIeKH8dVyDEr7S7wE3',  'effect',  'increase in pollen released by plants'),
('RO1J1OifvuO602qTIrSXdB',  'effect',  'increase in asthma complications'),
('RB7k7p2iQQgKdQrkRP2MZWM', 'effect',  'increase in disproportionate effects on children'),
('Ra98BRMZ0HlUpobb3Z0C5r',  'effect',  'increase in disproportionate effects on minority groups'),
('R9EmN8lJbIyQi0t6oj8e1w4', 'effect',  'greenhouse-gas externality'),
('RCtCTACPjLICXvxzHHsQ6o9', 'effect',  'builders are not required to check before building on a floodplain'),
('RDnngs7q3R6klffYKrfIIcZ', 'effect',  'deregulation'),
('R80q6o2vAd7r3ywEGhwmbDb', 'effect',  'increase in development of acute lower respiratory infection'),
('RB6zclWNN2qJW6OSyWjyfFz', 'effect',  'increase in lung cancer'),
('RC9893GbihwyuNWf6olyX2i', 'effect',  'ischaemic heart disease'),
('RGBfgwLkF3YDyhyGGb5HWL',  'effect',  'development of chronic obstructive pulmonary disease'),
('RrH4kPiYwZ0tSRSz4lnaYW',  'effect',  'increase in risk of stroke'),
('R892KwVv6vE4ZDULk8mz8S4', 'effect',  'change in salinity in oceans (both surface and subsurface)'),
('RBHHvT6sX3QbfYU2JlLhT5E', 'effect',  'increase in rain (and snow if cold enough) (precipitation)'),
('RByBIDdhul7eNMQVP3bYnfg', 'effect',  'drier soil during dry season'),
('R8IAmadbnqneVdqnTnrLuIU', 'effect',  'drier vegetation during dry season'),
('RCdI01J5CMbbjrTeJgTqHJv', 'effect',  'prolonged droughts'),
('RLc1ySxaRs4HWkW4m5w2Me',  'effect',  'increase in area burned by wildfire'),
('R4g51Eq3Q7uVWg9V5F5BTC',  'effect',  'increase in vegetation during wet season'),
('R7lbzoBwBLouLZawIp4Dioy', 'effect',  'lower salinity in freshwater'),
('R9HodVa8KHkIzJV3HunJ7HC', 'effect',  'increase in arctic and glacier ice melted by rain'),
('RBHUIy2I4ZBJSRGAvuInERX', 'effect',  'wetter soil during wet season'),
('R7UaBVCzh2O54oDnVl30shn', 'effect',  'increase in freshwater added to ocean'),
('RC908yZ4NQO8OtHHyOhBgj',  'effect',  'increase in sea level rise'),
('RDU23MRgHPOEAIMiIDo9xXj', 'effect',  'less sinking of cooling ocean water'),
('R8NBM1WXVHFjSNY6t1zM7C',  'effect',  'weakened ocean circulation (AMOC)'),
('RCoV5c1RuP5EGJ74GfyySDB', 'effect',  'less mixing of oxygenated water'),
('RDykfcwgFQkAwb8h12H5RoJ', 'effect',  'reduction in oxygen producing sea organisms'),
('RBO6QoxuN2QiowzfoEIVfUT', 'effect',  'decrease in dissolved oxygen in oceans'),
('RPRQOAoTZgGhrsmVpnIIrn',  'effect',  'increase in release of N2O and CH4 greenhouse gases'),
('R8ZTqebSrgr0Gg0fbTWSY3Y', 'effect',  'increase in N2O'),
('RBQIDI6zYf94WmhdxbT6WQ3', 'effect',  'increase in methane (CH4)'),
('R8znJBKduM7l8XDXMalSWSl', 'effect',  'increase in environmental migrants'),
('RBac6p7ap6Y8fZa4iZKUeG4', 'effect',  'less freezing conditions during winter'),
('RC1gWVzE8Q4jhyI84rXxuh8', 'effect',  'increase in tick winter survival'),
('RCbxy21PZJEKetM8Fk47kIM', 'effect',  'expansion in tick habitat'),
('RCy1sC1n7wY7RI3aIXYmhEX', 'effect',  'expansion of Lyme disease'),
('R8L1XYnGtXh6s2DKVRE6ymu', 'effect',  'increase in Lyme disease infection'),
('RBYAEANbzZXfxcNfkPYS1Um', 'effect',  'melting Greenland ice sheet'),
('RBraJKr6hbJU5awScQurmQE', 'effect',  'permafrost melt'),
('RDDtV325vfj73RkGBtEJcwJ', 'effect',  'lower Antarctic sea ice extent'),
('RfkjEXa4fTJvsuzk6ushUu',  'effect',  'retreat of glaciers (glacier melt)'),
('R8qf6iSMjTV548UCPjK3rvf', 'effect',  'lower oxygen able to dissolve in ocean (solubility)'),
('RCOKh8I57dfccKh5QTFhHB0', 'effect',  'warmer oceans'),
('RCDZl2bsYh3B1YlJUL7nRcM', 'effect',  'increase in ocean surface temperature'),
('RDjJKpBW9PimroTaLftSZS8', 'effect',  'expansion of oceans'),
('R1kRDiL29pcyXoNOkHduKB',  'effect',  'increase in marine heatwaves'),
('RcIHdxpjQwjr8EG8yMhEYV',  'effect',  'increase in hurricane strength'),
('R8JoXNnKTYqERwU7fblKTWB', 'effect',  'increase in hurricane costs'),
('R9x3oCu22QJK9ebw5xL7NvB', 'effect',  'increase in coral bleaching and destruction'),
('R9JAWzfiZ9haeNhHiCpTWkr', 'effect',  'decrease in tourism'),
('R5hC8Ud8449ZsdtwYdskf1',  'effect',  'coal mining'),
('RBIjeqALTDlfCzVLfBMq4EC', 'effect',  'burning coal'),
('RJNGfc0g7HO0V3kCM2R8bA',  'effect',  'increase in risk of stomach cancer'),
('RSqgmuB6RIAv04gEixDJOx',  'effect',  'burning fossil fuel for electricity production'),
('R8Es1gGVfBBLpoCGPWE48CV', 'effect',  'buildings and their construction, materials, gas heating, cooling, and refrigeration'),
('RBoKo0n5lpo1zk2uDMdZuab', 'effect',  'increase in HFCs and PFCs'),
('R8kybnu8AkaNkF2CcKTtPMk', 'effect',  'industrial activity'),
('R9ULHB1n9QqrbQRX5vv01hs', 'effect',  'cattle cow burps'),
('R9a1d8UGT12xJhW9F2fJ5Ql', 'effect',  'food waste, unhealthy agriculture, and deforestation'),
('RBzyxPGEWn768HIJJhTxIG',  'effect',  'fracking leaks'),
('RCpkare9aCROASttOpkDXpa', 'effect',  'human population growth'),
('RDjwXK2vPUuvsb5nJUvtTMC', 'effect',  'transporting people and goods'),
('R7T07NmeX8SYfysieiycbv4', 'myth',  'Corals are resilient to bleaching'),
('R7dTYeRXeW1jkqPzYRFE281', 'myth',  'Renewable energy is too expensive'),
('R7hFprQCCizIoO67xtr4tlq', 'myth',  'Animals and plants can adapt'),
('R8Qh5dLGvzYwFZpritPBmBh', 'myth',  'Coral atolls grow as sea levels rise'),
('R8Vn11VsfBxtxxsy5t4Ysza', 'myth',  'Renewable energy investment kills jobs'),
('R8ZhofBtOtoHDSFtEhoLGir', 'myth',  'Climate has changed before'),
('R9A0xjtcUkuktq4th33nDr1', 'myth',  'It hasn''t warmed since 1998'),
('R9wVHvf1lRnupW3NivH3YOe', 'myth',  'There''s no consensus'),
('RBPpD7IvyIMbCYHJqnNqfM0', 'myth',  'Hurricanes aren''t linked to global warming'),
('RCU0YwArp49u8Xyj0skNjXj', 'myth',  'Antarctica is gaining ice'),
('RCZyj3ljE4sg6vf5hphtud0', 'myth',  'It''s the sun'),
('RCqODufKJse3xkgAny5v5fI', 'myth',  'Temperature record is unreliable'),
('RCw8SmMRRaBEOoHqTzFvZml', 'myth',  'CO2 limits will hurt the poor'),
('RGoKTEGl49269XhVT2L5b7',  'myth',  'Renewables can''t provide baseload power'),
('RINEZk68x8Ej1HrbxpdbJK',  'myth',  'Climate models are unreliable'),
('RXlELjsOUaVbJqmvO91WFL',  'myth',  'It''s cooling'),
('Relkq8lNydWamAFggTD3RD',  'myth',  'It''s not bad'),
('Rs4yw1TXQsOysU3babN95H',  'myth',  'Wildfires aren''t caused by global warming'),
('R8tO6zSdeJRRUSPaznZIbKU', 'null',  'increase in greenhouse effect'),
('RDW2Jq9syvIdke0hdTNzGcu', 'null',  'person is elderly'),
('R881q5suJxwe7p0C9G6TnxQ', 'null',  'person is in a community likely without air conditioning'),
('RC77fWvhvLSUoDgysxzCyGk', 'null',  'person is outside often'),
('RMitjwsMYIFgaH1m0sVD8N',  'null',  'person is in the marines'),
('RCSp3Q6QJjaE6ehKKudHudg', 'null',  'Farming, Fishing, and Forestry Occupations'),
('R8GnjibSy3jN71u038XPlcj', 'null',  'lower stratospheric cooling'),
('R8WxponQcYpGf2zDnbsuVxG', 'solution',  'enact carbon tax policy (revenue neutral)'),
('RCFcpfKKeKFTkyBttzYtl1P', 'solution',  'effective communication framing'),
('RGvNz4i9rN6i6s2DETRSKD',  'solution',  'enact ranked-choice voting policy'),
('R9iV4b31x0p1xmG7jvYhBtq', 'solution',  'establish a federal green jobs program'),
('RCyBGt3EhMba7KSfwkbu9Yu', 'solution',  'enact cap and trade policy'),
('RKsHmIBffqClOO8UkcSmY3',  'solution',  'Increase in investment'),
('RCkLLIxnjRrEwqFDLGw9Phk', 'solution',  'increase in funding for suicide prevention'),
('R703RV857dpjFbW0mm37eW9', 'solution',  'increase in air conditioning'),
('R7gVDW5GAY8MLHKOrp03FZQ', 'solution',  'vote in elections'),
('R7ulwwwhiWzwZBpdI7t5Z1F', 'solution',  'increase in restoration of abandoned farmland'),
('R8ECf0I0zdW2MwEbGGbcBdK', 'solution',  'call representative'),
('R8fP9mjl5SFWS1C4cgTogFw', 'solution',  'increase in multistrata agroforestry'),
('R8oAxwMu8mlvB2RXEW9dVDm', 'solution',  'increase in managed grazing'),
('R9JRAY46e14dxAkfDjQdqgw', 'solution',  'increase in tree intercropping'),
('R9asiFQ7bVkymcqkQyMOpXn', 'solution',  'increase in conservation agriculture'),
('RBC1YyRghNLYujOkJxKOxPM', 'solution',  'increase in tropical forest restoration'),
('RBzQLT1NY7IWvJXCMxrPPTk', 'solution',  'eating lower down the food-chain (plant-rich diets)'),
('RDIPgn6wLGNvB8BmWhcn2BV', 'solution',  'increase rate of carbon tax'),
('RDXACa7DGh7OTyB1o1roCZO', 'solution',  'increase in restoration of temperate forests'),
('RDaR05qkCxdbQERBFVfmfFU', 'solution',  'increase in carbon capture and storage'),
('RDsBA6sw2PNZOr6WuF0MvpQ', 'solution',  'increase in tree plantations (on degraded land)'),
('RDtjtNVivtpYdE8v55DyKrG', 'solution',  'increase in silvopasture'),
('RDuMXs0QujFAkNFKJHaJ3BN', 'solution',  'increase in bamboo production'),
('Rew83THb8xDe4QJVYuuf8M',  'solution',  'increase in regenerative annual cropping'),
('Rogalh6vEmPn4UqI4lP2FL',  'solution',  'increase in perennial staple crops'),
('RDUpv4M8PM4HOKbZuVIB8tT', 'solution',  'increase in cholera vaccines'),
('RCxxWzxHUToYGLFTAH8Kntl', 'solution',  'avoid building on land that is or will become a floodplain'),
('R7yNIp2SSecEuyVj4gZxSHF', 'solution',  'regulation/laws that require assessment of floodplains for new buildings'),
('R9LbmQn2lAubsJN4nR1Sqzo', 'solution',  'increase in goats clearing brush'),
('R73ikCqnentdefiugeatpz8', 'solution',  'producing electricity via offshore wind turbines'),
('R8wipsAXfB4fo66FQYwubtd', 'solution',  'producing electricity via distributed solar photovoltaics'),
('R9R6552i4fn3XHKpoV8QTOx', 'solution',  'producing electricity via utility-scale solar photovoltaics'),
('RCYcuSVsndxr46dKMakicwT', 'solution',  'switching to LED light bulbs'),
('RCdoVWPmTIcdEyb6QfkEug0', 'solution',  'producing electricity via onshore wind turbines'),
('RCsF77Q9uljIZkHshMgkbQP', 'solution',  'producing electricity via concentrated solar power'),
('RBCQdAOKui38ytAIKZlpPN6', 'solution',  'installing smart thermostats'),
('RCCli7m3xUZupUS871jEn0g', 'solution',  'using improved clean cookstoves'),
('RCPtkdL8hc2qCEMAaSA3OO7', 'solution',  'using high-performance glass in windows'),
('RDanTqMAQyQ4nGzlrt0j7Bm', 'solution',  'insulating buildings better'),
('RqffG0pylVR4qW85eGwoPl',  'solution',  'using high-efficiency heat pumps'),
('RvgK3RWRb6dVpRniUARv0a',  'solution',  'using biogas for cooking'),
('R7YYQegAXeBWrNAya5IhSuk', 'solution',  'composting'),
('RBPwaJUGpFPOUthNxvZoC3m', 'solution',  'using alternative cement'),
('RBeBCvukdLNSe5AtnlJpQ1k', 'solution',  'recycling paper'),
('RCfL29vOLXc9ds8maBP7yyg', 'solution',  'using methane digesters'),
('RCg7BxIR9BolygeacF635tH', 'solution',  'recycling'),
('RCweDCBg9pAFqwN7Q9K30tY', 'solution',  'using alternative refrigerants'),
('RD2p6adaCZJE3WmtfZ0qrU7', 'solution',  'managing refrigerants better'),
('RCVZWPiALoEjnaCAwnkuB6k', 'solution',  'include 1% seaweed in diet for cows and cattle'),
('RBDaBHXLKs8slSr2bwVTl9v', 'solution',  'protecting and rewetting peatland'),
('RfqwmaY5oYx5PSw5fhhfPi',  'solution',  'reducing food waste'),
('R6zCdUFmA2mP62Gqfbm5sE',  'solution',  'carpooling'),
('R8PIEqhm36x0Y9CvkgJlidT', 'solution',  'making trucks more efficient'),
('R9SuseoJG7H6QeUEvZwLciQ', 'solution',  'using electric cars'),
('RDSZw453Ge76hYTvYEsaAwU', 'solution',  'making aviation more efficient'),
('RDZ1RURQFOc7YmgjswS5IW7', 'solution',  'making ocean shipping more efficient'),
('RDhpXXRQgYARY8ocN1e2tI',  'solution',  'using public transit'),
('RDkaEppVGpX8sI5LgbzH7Eu', 'solution',  'using high-speed rail'),
('RItKzuJSSFw9hXydUSVEJX',  'solution',  'using hybrid cars'),
('Rtctk1SGyY2raocnj6VJeg',  'solution',  'being telepresent or teleworking'),
('R97nKRRZWNs0SIxDhgsFAbe', 'solution',  'improving health and education')
;

INSERT INTO #dev_session_uuids
SELECT DISTINCT session_uuid
     , 'Dev Site'
  FROM analytics_data
 WHERE LEFT(page_url, 28) <> 'https://app.climatemind.org/'
   AND session_uuid NOT IN (SELECT session_uuid FROM #dev_session_uuids)
;

--not doing
-- --manually get dates for the climate feed for data before 2021-02-28
-- --first real users on 2021-02-11
-- SELECT DISTINCT
--        session_uuid
--      , CAST(event_timestamp AS DATE) AS event_date
--   INTO #soft_launch_sessions_w_clicks
--   FROM analytics_data
--  WHERE category = 'card'
--    AND action = 'card_click'
--    AND label = 'card_iri'
--    AND CAST(event_timestamp AS DATE) = CAST('2021-02-11' AS DATE)
-- ;

--distinct daily climate feed for the effect cards
--event_date was instrumented on 2021-02-28
-- SELECT DISTINCT 
--        cf.session_uuid
--      , effect_position
--      , effect_iri AS card_iri
--      , COALESCE(CAST(cf.event_timestamp AS DATE), s.event_date) AS event_date
--   --INTO #climate_feed_daily_prep
--   FROM climate_feed cf
--   LEFT JOIN #soft_launch_sessions_w_clicks AS s
--     ON s.session_uuid = cf.session_uuid
--  WHERE cf.event_timestamp IS NOT NULL
--     OR s.event_date IS NOT NULL
-- ;

--event_timestamp not instrumented until the 2021-02-28, 
--data before that is assigned 2021-02-27 (can be filtered out later) because it's misleading on a daily level
--this only applies to 5 session_uuids, which all appear to be dev sessions
SELECT DISTINCT 
       cf.session_uuid
     , COALESCE(d.test_removal_process, 'Real') AS test_removal_process
     , effect_position
     , effect_iri AS card_iri
     , COALESCE(CAST(cf.event_timestamp AS DATE), CAST('2021-02-27' AS DATE)) AS event_date
  INTO #climate_feed_daily_prep
  FROM climate_feed AS cf
  LEFT JOIN #dev_session_uuids AS d
    ON d.session_uuid = cf.session_uuid
;
--select count(distinct session_uuid);

--unique session dates
SELECT DISTINCT 
       session_uuid
     , event_date
  INTO #climate_feed_sessions
  FROM #climate_feed_daily_prep
;

--find next session date for each session_uuid
SELECT session_uuid
     , event_date
     , LEAD(event_date, 1, NULL) OVER (PARTITION BY session_uuid ORDER BY event_date) AS next_session_date
  INTO #next_session
  FROM #climate_feed_sessions
;

SELECT cfdp.session_uuid
     , cfdp.test_removal_process
     , cfdp.effect_position
     , cfdp.card_iri
     , cfdp.event_date
     , ns.next_session_date
  INTO #climate_feed_daily
  FROM #climate_feed_daily_prep AS cfdp
  JOIN #next_session AS ns
    ON cfdp.session_uuid = ns.session_uuid
   AND cfdp.event_date = ns.event_date
;

--Distinct card click events from the analtyics_data events table
--we do not care when or how many times the user clicks, just that they clicked
--card_click renamed to card_open with 2021-04-11 release
--to be consistent with page views. clicks before 2021-02-28 are set to 2021-02-27
SELECT DISTINCT
       session_uuid
     , value AS card_iri
     , CASE WHEN CAST(event_timestamp AS DATE) < CAST('2021-02-28' AS DATE)
            THEN CAST('2021-02-27' AS DATE)
            ELSE CAST(event_timestamp AS DATE) END AS event_date
  INTO #card_clicks_daily
  FROM analytics_data
 WHERE category = 'card'
   AND action IN ('card_click', 'card_open')
   AND label = 'card_iri'
   AND (LEFT(page_url, 28) = 'https://app.climatemind.org/' OR page_url IS NULL)
   --AND event_timestamp >= CAST('2021-02-11' AS DATE)
   --and session_uuid NOT IN (SELECT session_uuid FROM #dev_session_uuids)
;
-- select count (distinct session_uuid) from #card_clicks_daily;
 
-- select test_removal_process,  count(*), count(distinct c.session_uuid) 
-- select test_removal_process,  count(*), count(distinct c.session_uuid) 
-- from #card_clicks_daily c
-- join #dev_session_uuids d on c.session_uuid = d.session_uuid 
-- where event_date < CAST('2021-02-28' AS DATE) --236 58 before, 89 35 after ALL labeled as test
--  and card_iri in (select distinct effect_iri from climate_feed)
-- group by test_removal_process
--  --order by event_date;

-- --views and clicks
-- SELECT cfd.session_uuid
--      , cfd.effect_position
--      , cfd.card_iri
--      , cfd.event_date
--      , BOOL_OR(ccd.session_uuid IS NOT NULL) AS clicked_flag
--   -- INTO #climate_feed_daily_clicks
--   FROM #climate_feed_daily AS cfd
--   JOIN #card_clicks_daily AS ccd
--     ON cfd.session_uuid = ccd.session_uuid
--    AND ccd.event_date >= cfd.event_date
--    AND ccd.event_date < COALESCE(next_session_date, CAST('9999-12-31' AS DATE))
--  GROUP BY session_uuid, effect_position, card_iri, event_date
-- ;

--views and clicks (climate feed)
--this would normally be one query but I'm not sure how to do it with Azure
SELECT cfd.session_uuid
     , cfd.test_removal_process
     , cfd.effect_position
     , cfd.card_iri
     , cfd.event_date
     , clicks.clicked_flag
  INTO #climate_feed_daily_clicks
  FROM #climate_feed_daily AS cfd
  LEFT JOIN (
    SELECT session_uuid
         , effect_position
         , card_iri
         , event_date
         , 1 AS clicked_flag
      FROM #climate_feed_daily AS cfd
     WHERE EXISTS (SELECT 1
                     FROM #card_clicks_daily AS ccd
                    WHERE cfd.session_uuid = ccd.session_uuid
                      AND ccd.event_date >= cfd.event_date
                      AND ccd.event_date < COALESCE(next_session_date, CAST('9999-12-31' AS DATE))
                      AND cfd.card_iri = ccd.card_iri
                  )
     ) clicks
    ON cfd.session_uuid = clicks.session_uuid
   AND cfd.effect_position = clicks.effect_position
   AND cfd.card_iri = clicks.card_iri
   AND cfd.event_date = clicks.event_date
;

-- select test_removal_process, count(*), count(distinct session_uuid)
-- from #climate_feed_daily_clicks
-- where 1=1--test_removal_process = 'Real' 
-- and clicked_flag = 1 --event clicks only
-- group by test_removal_process
-- ;

--views and clicks (solution feed)
/* We don't have solution feed view instrumented. We also cannot tell if they clicked the solution 
on the solution feed or the effect card. So consider anyone that viewed the climate feed to have 
viewed the solution feed OR viewed the solution from an effect card*/
SELECT DISTINCT cfd.session_uuid
     , cfd.test_removal_process
     , NULL AS effect_position
     , n.card_iri
     , cfd.event_date
     , cfd.next_session_date
  INTO #solution_feed_daily
  FROM #climate_feed_daily AS cfd
  CROSS JOIN (SELECT card_iri
                FROM #climate_mind_nodes AS n
               WHERE type = 'solution'
             ) AS n
;

SELECT sfd.session_uuid
     , sfd.test_removal_process
     -- , sfd.effect_position
     , sfd.card_iri
     , sfd.event_date
     , clicks.clicked_flag
  INTO #solution_feed_daily_clicks
  FROM #solution_feed_daily AS sfd
  LEFT JOIN (
    SELECT session_uuid
         -- , effect_position
         , card_iri
         , event_date
         , 1 AS clicked_flag
      FROM #solution_feed_daily AS sfd
     WHERE EXISTS (SELECT 1
                     FROM #card_clicks_daily AS ccd
                    WHERE sfd.session_uuid = ccd.session_uuid
                      AND ccd.event_date >= sfd.event_date
                      AND ccd.event_date < COALESCE(sfd.next_session_date, CAST('9999-12-31' AS DATE))
                      AND sfd.card_iri = ccd.card_iri
                  )
     ) clicks
    ON sfd.session_uuid = clicks.session_uuid
   -- AND sfd.effect_position = clicks.effect_position
   AND sfd.card_iri = clicks.card_iri
   AND sfd.event_date = clicks.event_date
;

--top 3 values long form for for each session_uuid and date
--this could likely be done in an easier way in Python than SQL
--first create long form table
--each session only has one record in the scores table, so we don't need to use event date
SELECT * 
  INTO #scores_long_daily 
  FROM
(SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Security' AS value
     , security AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Conformity' AS value
     , conformity AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Benevolence' AS value
     , benevolence AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Tradition' AS value
     , tradition AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Universalism' AS value
     , universalism AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Self Direction' AS value
     , self_direction AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Stimulation' AS value
     , stimulation AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Hedonism' AS value
     , hedonism AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Achievement' AS value
     , achievement AS score
  FROM scores
UNION ALL
SELECT DISTINCT 
       session_uuid
     -- , CAST(scores_created_timestamp AS DATE) AS event_date
     , 'Power' AS value
     , power AS score
  FROM scores
)sub
;

--filter to top 3 by session and event date
--CREATE TABLE #top3_personal_value_sessions 
SELECT session_uuid
     -- , event_date
     , value AS top3_personal_value
  INTO #top3_personal_value_sessions
  FROM (SELECT session_uuid
             -- , event_date
             , value
             , ROW_NUMBER() OVER (PARTITION BY session_uuid ORDER BY score DESC) AS score_rank
          FROM #scores_long_daily
          )sub
 WHERE score_rank <= 3
;

--save as kpi_click_view_YYYY-MM-DD then update tableau
SELECT cfd.event_date
     , cfd.effect_position
     , cfd.test_removal_process
     , 'effect' AS card_type --only looking at effect cards right now, will add solutions and myths
     , cfd.card_iri
     , cfd.session_uuid
     , cfd.clicked_flag
  FROM #climate_feed_daily_clicks cfd
  UNION ALL
SELECT sfd.event_date
     , NULL AS effect_position
     , sfd.test_removal_process
     , 'solution' AS card_type --only looking at effect cards right now, will add solutions and myths
     , sfd.card_iri
     , sfd.session_uuid
     , sfd.clicked_flag
  FROM #solution_feed_daily_clicks sfd
;

--save as top3_personal_value_YYYY-MM-DD then comment out to get table above
SELECT * 
  FROM #top3_personal_value_sessions
 WHERE session_uuid IN (SELECT DISTINCT session_uuid FROM #climate_feed_daily_clicks)
;

/*
 --old agg table, now doing aggregations in Tableau
SELECT cfd.event_date
     , cfd.effect_position
     , cfd.test_removal_process
     , pv.top3_personal_value
     , 'effect' AS card_type --only looking at effect cards right now, will add solutions and myths
     , cfd.card_iri
     , COUNT(cfd.session_uuid) AS card_view_count --based on card loaded in climate feed
     , COUNT(cfd.clicked_flag)  AS card_click_count
  INTO #kpi_card_click
  FROM #top3_personal_value_sessions AS pv
  JOIN #climate_feed_daily_clicks cfd
    ON cfd.session_uuid = pv.session_uuid

  -- JOIN #climate_feed_daily AS cfd
  --   ON cfd.session_uuid = pv.session_uuid
  --  -- AND cfd.event_date = pv.event_date
  -- LEFT JOIN #card_clicks_daily AS ccd
  --   ON ccd.session_uuid = cfd.session_uuid
  --  -- AND ccd.event_date = cfd.event_date
  --  AND ccd.card_iri = cfd.card_iri

   GROUP BY 
   cfd.event_date
     , cfd.effect_position
     , cfd.test_removal_process
     , pv.top3_personal_value
     , cfd.card_iri
   ;

   select * from #kpi_card_click;
*/
