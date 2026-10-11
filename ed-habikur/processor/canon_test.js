const fs=require('fs');const crypto=require('crypto');
const canon = v => Array.isArray(v) ? "[" + v.map(canon).join(",") + "]" : (v && typeof v === "object") ? "{" + Object.keys(v).sort().map(k => JSON.stringify(k) + ":" + canon(v[k])).join(",") + "}" : JSON.stringify(v);
const v=JSON.parse(fs.readFileSync(process.argv[2]));const o=JSON.parse(fs.readFileSync(process.argv[3]));Object.assign(v,o);
const p={id:v.id??null,createdAt:v.createdAt??null,tech:v.tech??null,customer:v.customer??null,address:v.address??null,audioSha256:v.audio?.sha256??null,transcript:v.transcript??null,report:v.report??null,sealedAt:v.seal?.sealedAt??null};
console.log(crypto.createHash('sha256').update(canon(p)).digest('hex')===o.seal.hash?'MATCH':'MISMATCH');
