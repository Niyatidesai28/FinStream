# SAP interview bridge: FinStream

No ABAP, SAPUI5, Fiori, SAP MM or SAP GRC code exists here. The bridge is conceptual.

| SAP role requirement | Concrete project evidence | Practice next |
|---|---|---|
| Business rules and validation | AlertCreate constraints and inclusive thresholds | express a positive order-quantity rule with tests |
| Debug technical issues | Infinity caused serialization failure after storage | narrate reproduce -> isolate -> validate early -> regress |
| Application UI | React props/state and labeled alert form | learn UI5 model binding and controller event handlers |
| OOP | PriceGenerator/AlertService encapsulate state | compare public method vs private implementation in ABAP Objects |
| SQL/data modeling | no database implementation | do a separate relational schema/query exercise, label it learning |
| Test scripts/documentation | API/browser tests, contract and rollback docs | explain expected/actual/result and evidence |
| SDLC/code review | isolated audit branch and draft PR | inspect diff, test, review, then manually decide merge |

ABAP is SAP's business programming language with procedural and object-oriented constructs.
Start with typed variables, conditions, loops, classes and methods. An internal table stores
same-type rows in memory; it is not automatically a database table. A useful analogy is
FinStream's alert list, with stronger declared row types. [SAP ABAP introduction](https://learning.sap.com/courses/learn-the-basics-of-abap-programming-on-sap-btp/understanding-abap),
[SAP internal tables](https://learning.sap.com/courses/basic-abap-programming/working-with-simple-internal-tables_a4beb937-0c7b-45b9-92be-ff26a5159fad).

SAP Fiori describes user-experience principles; SAPUI5 is a JavaScript UI toolkit offering
controls, MVC and binding. React experience helps you reason about events and displayed
state, but its component model is not the same framework. Practice a UI5 list bound to a
small JSON model and explain what a controller does. [SAPUI5 documentation](https://help.sap.com/docs/SAPUI5/b2f662dd9d7a4ec680056733050b4d34/c179ca9886624eaba7d56115b4cc4a84.html).

For MM, learn the distinction between a purchase requisition (internal need), purchase
order (supplier order), goods receipt (received quantity) and invoice verification.
Threshold validation transfers as a business-rule skill, not as procurement experience.
[SAP procure-to-pay](https://learning.sap.com/courses/explaining-payables-invoice-processing/exploring-the-procure-to-pay-process_d7a4061e-3d6a-44ff-bab5-e548bc258dfc).

For GRC, learn least privilege, role design, access reviews and segregation of duties.
A shared unauthenticated alert API illustrates why ownership and authorization matter.
Separating conflicting responsibilities reduces access risk; CORS is not that control.
[SAP access risk context](https://help.sap.com/docs/SAP_ACCESS_CONTROL/5cae1bc9a72348389e91183714220e30/8716ea4f962a2e74e10000000a44176f.html).

Interview answers: “I have not developed SAP applications yet. I can demonstrate backend
validation, UI/API integration, test evidence and careful Git review in FinStream, and I
am learning how those skills map to SAP's language, UI and enterprise processes.”
Do not claim team collaboration history solely because a draft PR was created by this audit.
