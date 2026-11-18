const assert=require("node:assert/strict"),fs=require("node:fs"),vm=require("node:vm"),path=require("node:path");
let source=fs.readFileSync(path.join(__dirname,"../apps/sheets.js"),"utf8");
source=source.replace('EZOffice.register("sheets",','globalThis.__calculate=calculate;EZOffice.register("sheets",');
const sandbox={EZOffice:{register(){}}};vm.createContext(sandbox);vm.runInContext(source,sandbox);
const calc=sandbox.__calculate;
for(const [formula,want,extra] of [
["=IF(1,42,1/0)",42],["=IF(0,1/0,17)",17],
["=IF(1,IF(0,1/0,9),1/0)",9],
["=IF(1,3,B1)",3,["=A1"]],["=IF(0,B1,5)",5,["=A1"]],
["=IF(1,ROUND(10/3,2),SQRT(-1))",3.33],
["=IF(0,SUM(B1:B1),7)",7,["=A1"]]
])assert.equal(calc([[formula,...(extra||[])]],0,0),want,formula);
for(const [formula,error] of [["=IF(1,1/0,3)",/#DIV\/0!/],["=IF(1,2)",/#PARSE!/],["=IF(1,2,3,4)",/#PARSE!/]])assert.throws(()=>calc([[formula]],0,0),error);
console.log("10 lazy IF acceptance cases passed");