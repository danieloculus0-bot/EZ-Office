const assert=require("node:assert/strict");
const fs=require("node:fs"),vm=require("node:vm"),path=require("node:path");
let source=fs.readFileSync(path.join(__dirname,"../apps/sheets.js"),"utf8");
source=source.replace('EZOffice.register("sheets",','globalThis.__calculate=calculate;EZOffice.register("sheets",');
const sandbox={EZOffice:{register(){}}};
vm.createContext(sandbox);vm.runInContext(source,sandbox);
const calc=sandbox.__calculate;
const rows=[
  ["10","20","=A1<B1","=IF(A1<B1,100,1/0)"],
  ["=IF(2>=2,7,1/0)","=IF(2<>3,8,1/0)","=IF(2=2,9,1/0)","=IF(2!=3,10,1/0)"],
  ["=IF(4>3,11,1/0)","=IF(4<=4,12,1/0)","=IF((2+3)>4,13,1/0)","=IF(0,1/0,1<2)"],
  ["=1+2*3>=7","=IF(0,1/0<2,5)","=IF(1,2<3,1/0)","=IF(1,2,3)"]
];
for(const [r,c,want] of [[0,2,1],[0,3,100],[1,0,7],[1,1,8],[1,2,9],[1,3,10],[2,0,11],[2,1,12],[2,2,13],[2,3,1],[3,0,1],[3,1,5],[3,2,1],[3,3,2]])assert.equal(calc(rows,r,c),want,`case ${r}:${c}`);
for(const formula of ["=1<2<3","=IF(1<,2,3)"])assert.throws(()=>calc([[formula]],0,0),/#PARSE!/);
console.log("16 numeric comparison acceptance cases passed");
