import{r as C,j as p,s as I,a as P,F as ut,T as H,S as st,R as Wn,b as Yn,B as Me,c as Ua,d as Va}from"./index.9a67391e.js";const Un=C.exports.createContext({height:0,width:0});var Vn=(t=>(t[t.BP1=520]="BP1",t[t.BP2=900]="BP2",t))(Vn||{});const Ha=({children:t})=>{const[e,n]=C.exports.useState(window.innerWidth),[a,r]=C.exports.useState(window.innerHeight),i=()=>{n(window.innerWidth),r(window.innerHeight)};return C.exports.useEffect(()=>(window.addEventListener("resize",i),()=>window.removeEventListener("resize",i)),[]),p(Un.Provider,{value:{width:e,height:a},children:t})};/*! *****************************************************************************
Copyright (c) Microsoft Corporation.

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR
OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
PERFORMANCE OF THIS SOFTWARE.
***************************************************************************** */function Hn(t,e,n,a){function r(i){return i instanceof n?i:new n(function(o){o(i)})}return new(n||(n=Promise))(function(i,o){function s(u){try{f(a.next(u))}catch(c){o(c)}}function l(u){try{f(a.throw(u))}catch(c){o(c)}}function f(u){u.done?i(u.value):r(u.value).then(s,l)}f((a=a.apply(t,e||[])).next())})}function Bn(t,e){var n={label:0,sent:function(){if(i[0]&1)throw i[1];return i[1]},trys:[],ops:[]},a,r,i,o;return o={next:s(0),throw:s(1),return:s(2)},typeof Symbol=="function"&&(o[Symbol.iterator]=function(){return this}),o;function s(f){return function(u){return l([f,u])}}function l(f){if(a)throw new TypeError("Generator is already executing.");for(;n;)try{if(a=1,r&&(i=f[0]&2?r.return:f[0]?r.throw||((i=r.return)&&i.call(r),0):r.next)&&!(i=i.call(r,f[1])).done)return i;switch(r=0,i&&(f=[f[0]&2,i.value]),f[0]){case 0:case 1:i=f;break;case 4:return n.label++,{value:f[1],done:!1};case 5:n.label++,r=f[1],f=[0];continue;case 7:f=n.ops.pop(),n.trys.pop();continue;default:if(i=n.trys,!(i=i.length>0&&i[i.length-1])&&(f[0]===6||f[0]===2)){n=0;continue}if(f[0]===3&&(!i||f[1]>i[0]&&f[1]<i[3])){n.label=f[1];break}if(f[0]===6&&n.label<i[1]){n.label=i[1],i=f;break}if(i&&n.label<i[2]){n.label=i[2],n.ops.push(f);break}i[2]&&n.ops.pop(),n.trys.pop();continue}f=e.call(t,n)}catch(u){f=[6,u],r=0}finally{a=i=0}if(f[0]&5)throw f[1];return{value:f[0]?f[1]:void 0,done:!0}}}var B=function(){},N=B(),Et=Object,$=function(t){return t===N},nt=function(t){return typeof t=="function"},q=function(t,e){return Et.assign({},t,e)},Le="undefined",De=function(){return typeof window!=Le},Ba=function(){return typeof document!=Le},Ga=function(){return De()&&typeof window.requestAnimationFrame!=Le},Dt=new WeakMap,Xa=0,Nt=function(t){var e=typeof t,n=t&&t.constructor,a=n==Date,r,i;if(Et(t)===t&&!a&&n!=RegExp){if(r=Dt.get(t),r)return r;if(r=++Xa+"~",Dt.set(t,r),n==Array){for(r="@",i=0;i<t.length;i++)r+=Nt(t[i])+",";Dt.set(t,r)}if(n==Et){r="#";for(var o=Et.keys(t).sort();!$(i=o.pop());)$(t[i])||(r+=i+":"+Nt(t[i])+",");Dt.set(t,r)}}else r=a?t.toJSON():e=="symbol"?t.toString():e=="string"?JSON.stringify(t):""+t;return r},ve=!0,qa=function(){return ve},Gn=De(),ze=Ba(),pe=Gn&&window.addEventListener?window.addEventListener.bind(window):B,Ka=ze?document.addEventListener.bind(document):B,be=Gn&&window.removeEventListener?window.removeEventListener.bind(window):B,Ja=ze?document.removeEventListener.bind(document):B,Qa=function(){var t=ze&&document.visibilityState;return $(t)||t!=="hidden"},Za=function(t){return Ka("visibilitychange",t),pe("focus",t),function(){Ja("visibilitychange",t),be("focus",t)}},tr=function(t){var e=function(){ve=!0,t()},n=function(){ve=!1};return pe("online",e),pe("offline",n),function(){be("online",e),be("offline",n)}},er={isOnline:qa,isVisible:Qa},nr={initFocus:Za,initReconnect:tr},Xt=!De()||"Deno"in window,ar=function(t){return Ga()?window.requestAnimationFrame(t):setTimeout(t,1)},Tt=Xt?C.exports.useEffect:C.exports.useLayoutEffect,oe=typeof navigator!="undefined"&&navigator.connection,an=!Xt&&oe&&(["slow-2g","2g"].includes(oe.effectiveType)||oe.saveData),Xn=function(t){if(nt(t))try{t=t()}catch{t=""}var e=[].concat(t);t=typeof t=="string"?t:(Array.isArray(t)?t.length:t)?Nt(t):"";var n=t?"$swr$"+t:"";return[t,e,n]},lt=new WeakMap,qn=0,Kn=1,Jn=2,It=function(t,e,n,a,r,i,o){o===void 0&&(o=!0);var s=lt.get(t),l=s[0],f=s[1],u=s[3],c=l[e],v=f[e];if(o&&v)for(var g=0;g<v.length;++g)v[g](n,a,r);return i&&(delete u[e],c&&c[0])?c[0](Jn).then(function(){return t.get(e)}):t.get(e)},rr=0,he=function(){return++rr},Qn=function(){for(var t=[],e=0;e<arguments.length;e++)t[e]=arguments[e];return Hn(void 0,void 0,void 0,function(){var n,a,r,i,o,s,l,f,u,c,v,g,O,x,h,m,A,k,T,w,R;return Bn(this,function(M){switch(M.label){case 0:if(n=t[0],a=t[1],r=t[2],i=t[3],o=typeof i=="boolean"?{revalidate:i}:i||{},s=$(o.populateCache)?!0:o.populateCache,l=o.revalidate!==!1,f=o.rollbackOnError!==!1,u=o.optimisticData,c=Xn(a),v=c[0],g=c[2],!v)return[2];if(O=lt.get(n),x=O[2],t.length<3)return[2,It(n,v,n.get(v),N,N,l,!0)];if(h=r,A=he(),x[v]=[A,0],k=!$(u),T=n.get(v),k&&(w=nt(u)?u(T):u,n.set(v,w),It(n,v,w)),nt(h))try{h=h(n.get(v))}catch(L){m=L}return h&&nt(h.then)?[4,h.catch(function(L){m=L})]:[3,2];case 1:if(h=M.sent(),A!==x[v][0]){if(m)throw m;return[2,h]}else m&&k&&f&&(s=!0,h=T,n.set(v,T));M.label=2;case 2:return s&&(m||(nt(s)&&(h=s(h,T)),n.set(v,h)),n.set(g,q(n.get(g),{error:m}))),x[v][1]=he(),[4,It(n,v,h,m,N,l,!!s)];case 3:if(R=M.sent(),m)throw m;return[2,s?R:h]}})})},rn=function(t,e){for(var n in t)t[n][0]&&t[n][0](e)},Zn=function(t,e){if(!lt.has(t)){var n=q(nr,e),a={},r=Qn.bind(N,t),i=B;if(lt.set(t,[a,{},{},{},r]),!Xt){var o=n.initFocus(setTimeout.bind(N,rn.bind(N,a,qn))),s=n.initReconnect(setTimeout.bind(N,rn.bind(N,a,Kn)));i=function(){o&&o(),s&&s(),lt.delete(t)}}return[t,r,i]}return[t,lt.get(t)[4]]},ir=function(t,e,n,a,r){var i=n.errorRetryCount,o=r.retryCount,s=~~((Math.random()+.5)*(1<<(o<8?o:8)))*n.errorRetryInterval;!$(i)&&o>i||setTimeout(a,s,r)},ta=Zn(new Map),ea=ta[0],or=ta[1],na=q({onLoadingSlow:B,onSuccess:B,onError:B,onErrorRetry:ir,onDiscarded:B,revalidateOnFocus:!0,revalidateOnReconnect:!0,revalidateIfStale:!0,shouldRetryOnError:!0,errorRetryInterval:an?1e4:5e3,focusThrottleInterval:5*1e3,dedupingInterval:2*1e3,loadingTimeout:an?5e3:3e3,compare:function(t,e){return Nt(t)==Nt(e)},isPaused:function(){return!1},cache:ea,mutate:or,fallback:{}},er),aa=function(t,e){var n=q(t,e);if(e){var a=t.use,r=t.fallback,i=e.use,o=e.fallback;a&&i&&(n.use=a.concat(i)),r&&o&&(n.fallback=q(r,o))}return n},ge=C.exports.createContext({}),sr=function(t){var e=t.value,n=aa(C.exports.useContext(ge),e),a=e&&e.provider,r=C.exports.useState(function(){return a?Zn(a(n.cache||ea),e):N})[0];return r&&(n.cache=r[0],n.mutate=r[1]),Tt(function(){return r?r[2]:N},[]),C.exports.createElement(ge.Provider,q(t,{value:n}))},lr=function(t,e){var n=C.exports.useState({})[1],a=C.exports.useRef(t),r=C.exports.useRef({data:!1,error:!1,isValidating:!1}),i=C.exports.useCallback(function(o){var s=!1,l=a.current;for(var f in o){var u=f;l[u]!==o[u]&&(l[u]=o[u],r.current[u]&&(s=!0))}s&&!e.current&&n({})},[]);return Tt(function(){a.current=t}),[a,r.current,i]},fr=function(t){return nt(t[1])?[t[0],t[1],t[2]||{}]:[t[0],null,(t[1]===null?t[2]:t[1])||{}]},ur=function(){return q(na,C.exports.useContext(ge))},cr=function(t){return function(){for(var n=[],a=0;a<arguments.length;a++)n[a]=arguments[a];var r=ur(),i=fr(n),o=i[0],s=i[1],l=i[2],f=aa(r,l),u=t,c=f.use;if(c)for(var v=c.length;v-- >0;)u=c[v](u);return u(o,s||f.fetcher,f)}},on=function(t,e,n){var a=e[t]||(e[t]=[]);return a.push(n),function(){var r=a.indexOf(n);r>=0&&(a[r]=a[a.length-1],a.pop())}},se={dedupe:!0},dr=function(t,e,n){var a=n.cache,r=n.compare,i=n.fallbackData,o=n.suspense,s=n.revalidateOnMount,l=n.refreshInterval,f=n.refreshWhenHidden,u=n.refreshWhenOffline,c=lt.get(a),v=c[0],g=c[1],O=c[2],x=c[3],h=Xn(t),m=h[0],A=h[1],k=h[2],T=C.exports.useRef(!1),w=C.exports.useRef(!1),R=C.exports.useRef(m),M=C.exports.useRef(e),L=C.exports.useRef(n),E=function(){return L.current},te=function(){return E().isVisible()&&E().isOnline()},Mt=function(F){return a.set(k,q(a.get(k),F))},Qe=a.get(m),Fa=$(i)?n.fallback[m]:i,X=$(Qe)?Fa:Qe,Ze=a.get(k)||{},xt=Ze.error,tn=!T.current,en=function(){return tn&&!$(s)?s:E().isPaused()?!1:o?$(X)?!1:n.revalidateIfStale:$(X)||n.revalidateIfStale},Wa=function(){return!m||!e?!1:Ze.isValidating?!0:tn&&en()},ee=Wa(),ne=lr({data:X,error:xt,isValidating:ee},w),vt=ne[0],ae=ne[1],Lt=ne[2],ot=C.exports.useCallback(function(F){return Hn(void 0,void 0,void 0,function(){var z,j,W,kt,Ct,U,_,tt,V,re,At,pt,ie;return Bn(this,function(Ot){switch(Ot.label){case 0:if(z=M.current,!m||!z||w.current||E().isPaused())return[2,!1];kt=!0,Ct=F||{},U=!x[m]||!Ct.dedupe,_=function(){return!w.current&&m===R.current&&T.current},tt=function(){var nn=x[m];nn&&nn[1]===W&&delete x[m]},V={isValidating:!1},re=function(){Mt({isValidating:!1}),_()&&Lt(V)},Mt({isValidating:!0}),Lt({isValidating:!0}),Ot.label=1;case 1:return Ot.trys.push([1,3,,4]),U&&(It(a,m,vt.current.data,vt.current.error,!0),n.loadingTimeout&&!a.get(m)&&setTimeout(function(){kt&&_()&&E().onLoadingSlow(m,n)},n.loadingTimeout),x[m]=[z.apply(void 0,A),he()]),ie=x[m],j=ie[0],W=ie[1],[4,j];case 2:return j=Ot.sent(),U&&setTimeout(tt,n.dedupingInterval),!x[m]||x[m][1]!==W?(U&&_()&&E().onDiscarded(m),[2,!1]):(Mt({error:N}),V.error=N,At=O[m],!$(At)&&(W<=At[0]||W<=At[1]||At[1]===0)?(re(),U&&_()&&E().onDiscarded(m),[2,!1]):(r(vt.current.data,j)?V.data=vt.current.data:V.data=j,r(a.get(m),j)||a.set(m,j),U&&_()&&E().onSuccess(j,m,n),[3,4]));case 3:return pt=Ot.sent(),tt(),E().isPaused()||(Mt({error:pt}),V.error=pt,U&&_()&&(E().onError(pt,m,n),(typeof n.shouldRetryOnError=="boolean"&&n.shouldRetryOnError||nt(n.shouldRetryOnError)&&n.shouldRetryOnError(pt))&&te()&&E().onErrorRetry(pt,m,n,ot,{retryCount:(Ct.retryCount||0)+1,dedupe:!0}))),[3,4];case 4:return kt=!1,re(),_()&&U&&It(a,m,V.data,V.error,!1),[2,!0]}})})},[m]),Ya=C.exports.useCallback(Qn.bind(N,a,function(){return R.current}),[]);if(Tt(function(){M.current=e,L.current=n}),Tt(function(){if(!!m){var F=m!==R.current,z=ot.bind(N,se),j=function(_,tt,V){Lt(q({error:tt,isValidating:V},r(vt.current.data,_)?N:{data:_}))},W=0,kt=function(_){if(_==qn){var tt=Date.now();E().revalidateOnFocus&&tt>W&&te()&&(W=tt+E().focusThrottleInterval,z())}else if(_==Kn)E().revalidateOnReconnect&&te()&&z();else if(_==Jn)return ot()},Ct=on(m,g,j),U=on(m,v,kt);return w.current=!1,R.current=m,T.current=!0,F&&Lt({data:X,error:xt,isValidating:ee}),en()&&($(X)||Xt?z():ar(z)),function(){w.current=!0,Ct(),U()}}},[m,ot]),Tt(function(){var F;function z(){var W=nt(l)?l(X):l;W&&F!==-1&&(F=setTimeout(j,W))}function j(){!vt.current.error&&(f||E().isVisible())&&(u||E().isOnline())?ot(se).then(z):z()}return z(),function(){F&&(clearTimeout(F),F=-1)}},[l,f,u,ot]),C.exports.useDebugValue(X),o&&$(X)&&m)throw M.current=e,L.current=n,w.current=!1,$(xt)?ot(se):xt;return{mutate:Ya,get data(){return ae.data=!0,X},get error(){return ae.error=!0,xt},get isValidating(){return ae.isValidating=!0,ee}}};Et.defineProperty(sr,"default",{value:na});var mr=cr(dr);const sn=I("h2",{color:"$primaryDark",variants:{size:{small:{fontSize:"$2",fontWeight:"$big"},medium:{fontSize:"$3",fontWeight:"$big"},large:{fontSize:"$5",lineHeight:"24px",fontWeight:"$big"}}},defaultVariants:{size:"medium"}}),le=I("h1",{fontWeight:"$semiBold",fontSize:"$4",variants:{color:{dark:{color:"$primaryDark"},light:{color:"$white"}},margin:{none:{margin:0}}},defaultVariants:{color:"dark"}}),vr=I("h2",{fontWeight:"$semiBold",fontSize:"$3",variants:{color:{dark:{color:"$primaryDark"},light:{color:"$white"}},margin:{none:{margin:0}}},defaultVariants:{color:"dark"}}),ye=I("strong",{fontSize:"inherit",color:"inherit",fontWeight:"$semiBold"}),Yt=I("a",{textDecoration:"none",fontSize:"inherit",fontWeight:"inherit",variants:{color:{white:{color:"$white","&:hover":{color:"$primaryPurple",transition:"color 0.1s ease"}},blue:{color:"$linkBlue"},purple:{color:"$primaryPurple"}},weight:{normal:{fontWeight:"$normal"},semiBold:{fontWeight:"$semiBold"}}}}),ln=I("div",{width:"fit-content",backgroundColor:"$lightGray",padding:"$2",whiteSpace:"pre-wrap",fontFamily:"monospace",fontSize:"$3"}),pr=`import databutton as db
import streamlit as st

@db.apps.streamlit(route="/app", name="My App")
def app():
    st.title("My app")

@db.jobs.repeat_every(seconds=60, name="My Job")
def job():
    # Something amazing here
    print("Success!")
`,br="$ databutton deploy",hr=({localOrCloud:t,editButton:e,deleteButton:n})=>t==="local"?P(ut,{children:[p(sn,{size:"large",children:"Oh, this project seems a bit empty"}),p(H,{children:"To add components to your project add one of the following decorators to any of your .py-files and they will magically appear here"}),p(st,{height:"small"}),p(ln,{children:pr}),p(st,{height:"small"}),P(H,{children:["To learn more about Databutton head over to our"," ",p(Yt,{href:"https://docs.databutton.com",target:"_blank",rel:"noreferrer",color:"blue",children:"documentation"})]})]}):P(ut,{children:[p(sn,{size:"large",children:"Oh, this project seems not to have been deployed yet."}),p(H,{children:"To deploy your project, navigate to your project folder and enter the following command."}),p(st,{height:"small"}),p(ln,{children:br}),p(st,{height:"small"}),P(H,{children:["To learn more about Databutton,"," ",p(Yt,{color:"blue",href:"https://docs.databutton.com",target:"_blank",rel:"noreferrer",children:"head over to our documentation"}),"."]}),p(st,{}),P(Wn,{children:[e,n]})]}),gr=I("div",{display:"flex",flexFlow:"column",padding:"$2",variants:{width:{full:{width:"100%"},"one-half":{width:"50%"},"one-third":{width:"33%"},"one-fourth":{width:"25%"}},align:{center:{margin:"0 auto"}}},defaultVariants:{width:"full"}});/*!
 * Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com
 * License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License)
 * Copyright 2022 Fonticons, Inc.
 */var yr={prefix:"fas",iconName:"rocket",icon:[512,512,[],"f135","M156.6 384.9L125.7 353.1C117.2 345.5 114.2 333.1 117.1 321.8C120.1 312.9 124.1 301.3 129.8 288H24C15.38 288 7.414 283.4 3.146 275.9C-1.123 268.4-1.042 259.2 3.357 251.8L55.83 163.3C68.79 141.4 92.33 127.1 117.8 127.1H200C202.4 124 204.8 120.3 207.2 116.7C289.1-4.07 411.1-8.142 483.9 5.275C495.6 7.414 504.6 16.43 506.7 28.06C520.1 100.9 516.1 222.9 395.3 304.8C391.8 307.2 387.1 309.6 384 311.1V394.2C384 419.7 370.6 443.2 348.7 456.2L260.2 508.6C252.8 513 243.6 513.1 236.1 508.9C228.6 504.6 224 496.6 224 488V380.8C209.9 385.6 197.6 389.7 188.3 392.7C177.1 396.3 164.9 393.2 156.6 384.9V384.9zM384 167.1C406.1 167.1 424 150.1 424 127.1C424 105.9 406.1 87.1 384 87.1C361.9 87.1 344 105.9 344 127.1C344 150.1 361.9 167.1 384 167.1z"]},wr={prefix:"fas",iconName:"stopwatch",icon:[448,512,[9201],"f2f2","M272 0C289.7 0 304 14.33 304 32C304 49.67 289.7 64 272 64H256V98.45C293.5 104.2 327.7 120 355.7 143L377.4 121.4C389.9 108.9 410.1 108.9 422.6 121.4C435.1 133.9 435.1 154.1 422.6 166.6L398.5 190.8C419.7 223.3 432 262.2 432 304C432 418.9 338.9 512 224 512C109.1 512 16 418.9 16 304C16 200 92.32 113.8 192 98.45V64H176C158.3 64 144 49.67 144 32C144 14.33 158.3 0 176 0L272 0zM248 192C248 178.7 237.3 168 224 168C210.7 168 200 178.7 200 192V320C200 333.3 210.7 344 224 344C237.3 344 248 333.3 248 320V192z"]},xr={prefix:"fas",iconName:"xmark",icon:[320,512,[128473,10005,10006,10060,215,"close","multiply","remove","times"],"f00d","M310.6 361.4c12.5 12.5 12.5 32.75 0 45.25C304.4 412.9 296.2 416 288 416s-16.38-3.125-22.62-9.375L160 301.3L54.63 406.6C48.38 412.9 40.19 416 32 416S15.63 412.9 9.375 406.6c-12.5-12.5-12.5-32.75 0-45.25l105.4-105.4L9.375 150.6c-12.5-12.5-12.5-32.75 0-45.25s32.75-12.5 45.25 0L160 210.8l105.4-105.4c12.5-12.5 32.75-12.5 45.25 0s12.5 32.75 0 45.25l-105.4 105.4L310.6 361.4z"]};/*!
 * Font Awesome Free 6.1.1 by @fontawesome - https://fontawesome.com
 * License - https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT License)
 * Copyright 2022 Fonticons, Inc.
 */function fn(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(t);e&&(a=a.filter(function(r){return Object.getOwnPropertyDescriptor(t,r).enumerable})),n.push.apply(n,a)}return n}function d(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?arguments[e]:{};e%2?fn(Object(n),!0).forEach(function(a){Ar(t,a,n[a])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):fn(Object(n)).forEach(function(a){Object.defineProperty(t,a,Object.getOwnPropertyDescriptor(n,a))})}return t}function Ut(t){return Ut=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},Ut(t)}function kr(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function un(t,e){for(var n=0;n<e.length;n++){var a=e[n];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(t,a.key,a)}}function Cr(t,e,n){return e&&un(t.prototype,e),n&&un(t,n),Object.defineProperty(t,"prototype",{writable:!1}),t}function Ar(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}function je(t,e){return Sr(t)||Tr(t,e)||ra(t,e)||Pr()}function qt(t){return Or(t)||Er(t)||ra(t)||Ir()}function Or(t){if(Array.isArray(t))return we(t)}function Sr(t){if(Array.isArray(t))return t}function Er(t){if(typeof Symbol!="undefined"&&t[Symbol.iterator]!=null||t["@@iterator"]!=null)return Array.from(t)}function Tr(t,e){var n=t==null?null:typeof Symbol!="undefined"&&t[Symbol.iterator]||t["@@iterator"];if(n!=null){var a=[],r=!0,i=!1,o,s;try{for(n=n.call(t);!(r=(o=n.next()).done)&&(a.push(o.value),!(e&&a.length===e));r=!0);}catch(l){i=!0,s=l}finally{try{!r&&n.return!=null&&n.return()}finally{if(i)throw s}}return a}}function ra(t,e){if(!!t){if(typeof t=="string")return we(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);if(n==="Object"&&t.constructor&&(n=t.constructor.name),n==="Map"||n==="Set")return Array.from(t);if(n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return we(t,e)}}function we(t,e){(e==null||e>t.length)&&(e=t.length);for(var n=0,a=new Array(e);n<e;n++)a[n]=t[n];return a}function Ir(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function Pr(){throw new TypeError(`Invalid attempt to destructure non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}var cn=function(){},Fe={},ia={},oa=null,sa={mark:cn,measure:cn};try{typeof window!="undefined"&&(Fe=window),typeof document!="undefined"&&(ia=document),typeof MutationObserver!="undefined"&&(oa=MutationObserver),typeof performance!="undefined"&&(sa=performance)}catch{}var Rr=Fe.navigator||{},dn=Rr.userAgent,mn=dn===void 0?"":dn,rt=Fe,S=ia,vn=oa,zt=sa;rt.document;var Z=!!S.documentElement&&!!S.head&&typeof S.addEventListener=="function"&&typeof S.createElement=="function",la=~mn.indexOf("MSIE")||~mn.indexOf("Trident/"),K="___FONT_AWESOME___",xe=16,fa="fa",ua="svg-inline--fa",ct="data-fa-i2svg",ke="data-fa-pseudo-element",Nr="data-fa-pseudo-element-pending",We="data-prefix",Ye="data-icon",pn="fontawesome-i2svg",_r="async",$r=["HTML","HEAD","STYLE","SCRIPT"],ca=function(){try{return!0}catch{return!1}}(),Ue={fas:"solid","fa-solid":"solid",far:"regular","fa-regular":"regular",fal:"light","fa-light":"light",fat:"thin","fa-thin":"thin",fad:"duotone","fa-duotone":"duotone",fab:"brands","fa-brands":"brands",fak:"kit","fa-kit":"kit",fa:"solid"},Vt={solid:"fas",regular:"far",light:"fal",thin:"fat",duotone:"fad",brands:"fab",kit:"fak"},da={fab:"fa-brands",fad:"fa-duotone",fak:"fa-kit",fal:"fa-light",far:"fa-regular",fas:"fa-solid",fat:"fa-thin"},Mr={"fa-brands":"fab","fa-duotone":"fad","fa-kit":"fak","fa-light":"fal","fa-regular":"far","fa-solid":"fas","fa-thin":"fat"},Lr=/fa[srltdbk\-\ ]/,ma="fa-layers-text",Dr=/Font ?Awesome ?([56 ]*)(Solid|Regular|Light|Thin|Duotone|Brands|Free|Pro|Kit)?.*/i,zr={"900":"fas","400":"far",normal:"far","300":"fal","100":"fat"},va=[1,2,3,4,5,6,7,8,9,10],jr=va.concat([11,12,13,14,15,16,17,18,19,20]),Fr=["class","data-prefix","data-icon","data-fa-transform","data-fa-mask"],ft={GROUP:"duotone-group",SWAP_OPACITY:"swap-opacity",PRIMARY:"primary",SECONDARY:"secondary"},Wr=[].concat(qt(Object.keys(Vt)),["2xs","xs","sm","lg","xl","2xl","beat","border","fade","beat-fade","bounce","flip-both","flip-horizontal","flip-vertical","flip","fw","inverse","layers-counter","layers-text","layers","li","pull-left","pull-right","pulse","rotate-180","rotate-270","rotate-90","rotate-by","shake","spin-pulse","spin-reverse","spin","stack-1x","stack-2x","stack","ul",ft.GROUP,ft.SWAP_OPACITY,ft.PRIMARY,ft.SECONDARY]).concat(va.map(function(t){return"".concat(t,"x")})).concat(jr.map(function(t){return"w-".concat(t)})),pa=rt.FontAwesomeConfig||{};function Yr(t){var e=S.querySelector("script["+t+"]");if(e)return e.getAttribute(t)}function Ur(t){return t===""?!0:t==="false"?!1:t==="true"?!0:t}if(S&&typeof S.querySelector=="function"){var Vr=[["data-family-prefix","familyPrefix"],["data-style-default","styleDefault"],["data-replacement-class","replacementClass"],["data-auto-replace-svg","autoReplaceSvg"],["data-auto-add-css","autoAddCss"],["data-auto-a11y","autoA11y"],["data-search-pseudo-elements","searchPseudoElements"],["data-observe-mutations","observeMutations"],["data-mutate-approach","mutateApproach"],["data-keep-original-source","keepOriginalSource"],["data-measure-performance","measurePerformance"],["data-show-missing-icons","showMissingIcons"]];Vr.forEach(function(t){var e=je(t,2),n=e[0],a=e[1],r=Ur(Yr(n));r!=null&&(pa[a]=r)})}var Hr={familyPrefix:fa,styleDefault:"solid",replacementClass:ua,autoReplaceSvg:!0,autoAddCss:!0,autoA11y:!0,searchPseudoElements:!1,observeMutations:!0,mutateApproach:"async",keepOriginalSource:!0,measurePerformance:!1,showMissingIcons:!0},Pt=d(d({},Hr),pa);Pt.autoReplaceSvg||(Pt.observeMutations=!1);var b={};Object.keys(Pt).forEach(function(t){Object.defineProperty(b,t,{enumerable:!0,set:function(n){Pt[t]=n,jt.forEach(function(a){return a(b)})},get:function(){return Pt[t]}})});rt.FontAwesomeConfig=b;var jt=[];function Br(t){return jt.push(t),function(){jt.splice(jt.indexOf(t),1)}}var et=xe,G={size:16,x:0,y:0,rotate:0,flipX:!1,flipY:!1};function Gr(t){if(!(!t||!Z)){var e=S.createElement("style");e.setAttribute("type","text/css"),e.innerHTML=t;for(var n=S.head.childNodes,a=null,r=n.length-1;r>-1;r--){var i=n[r],o=(i.tagName||"").toUpperCase();["STYLE","LINK"].indexOf(o)>-1&&(a=i)}return S.head.insertBefore(e,a),t}}var Xr="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ";function _t(){for(var t=12,e="";t-- >0;)e+=Xr[Math.random()*62|0];return e}function wt(t){for(var e=[],n=(t||[]).length>>>0;n--;)e[n]=t[n];return e}function Ve(t){return t.classList?wt(t.classList):(t.getAttribute("class")||"").split(" ").filter(function(e){return e})}function ba(t){return"".concat(t).replace(/&/g,"&amp;").replace(/"/g,"&quot;").replace(/'/g,"&#39;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}function qr(t){return Object.keys(t||{}).reduce(function(e,n){return e+"".concat(n,'="').concat(ba(t[n]),'" ')},"").trim()}function Kt(t){return Object.keys(t||{}).reduce(function(e,n){return e+"".concat(n,": ").concat(t[n].trim(),";")},"")}function He(t){return t.size!==G.size||t.x!==G.x||t.y!==G.y||t.rotate!==G.rotate||t.flipX||t.flipY}function Kr(t){var e=t.transform,n=t.containerWidth,a=t.iconWidth,r={transform:"translate(".concat(n/2," 256)")},i="translate(".concat(e.x*32,", ").concat(e.y*32,") "),o="scale(".concat(e.size/16*(e.flipX?-1:1),", ").concat(e.size/16*(e.flipY?-1:1),") "),s="rotate(".concat(e.rotate," 0 0)"),l={transform:"".concat(i," ").concat(o," ").concat(s)},f={transform:"translate(".concat(a/2*-1," -256)")};return{outer:r,inner:l,path:f}}function Jr(t){var e=t.transform,n=t.width,a=n===void 0?xe:n,r=t.height,i=r===void 0?xe:r,o=t.startCentered,s=o===void 0?!1:o,l="";return s&&la?l+="translate(".concat(e.x/et-a/2,"em, ").concat(e.y/et-i/2,"em) "):s?l+="translate(calc(-50% + ".concat(e.x/et,"em), calc(-50% + ").concat(e.y/et,"em)) "):l+="translate(".concat(e.x/et,"em, ").concat(e.y/et,"em) "),l+="scale(".concat(e.size/et*(e.flipX?-1:1),", ").concat(e.size/et*(e.flipY?-1:1),") "),l+="rotate(".concat(e.rotate,"deg) "),l}var Qr=`:root, :host {
  --fa-font-solid: normal 900 1em/1 "Font Awesome 6 Solid";
  --fa-font-regular: normal 400 1em/1 "Font Awesome 6 Regular";
  --fa-font-light: normal 300 1em/1 "Font Awesome 6 Light";
  --fa-font-thin: normal 100 1em/1 "Font Awesome 6 Thin";
  --fa-font-duotone: normal 900 1em/1 "Font Awesome 6 Duotone";
  --fa-font-brands: normal 400 1em/1 "Font Awesome 6 Brands";
}

svg:not(:root).svg-inline--fa, svg:not(:host).svg-inline--fa {
  overflow: visible;
  box-sizing: content-box;
}

.svg-inline--fa {
  display: var(--fa-display, inline-block);
  height: 1em;
  overflow: visible;
  vertical-align: -0.125em;
}
.svg-inline--fa.fa-2xs {
  vertical-align: 0.1em;
}
.svg-inline--fa.fa-xs {
  vertical-align: 0em;
}
.svg-inline--fa.fa-sm {
  vertical-align: -0.0714285705em;
}
.svg-inline--fa.fa-lg {
  vertical-align: -0.2em;
}
.svg-inline--fa.fa-xl {
  vertical-align: -0.25em;
}
.svg-inline--fa.fa-2xl {
  vertical-align: -0.3125em;
}
.svg-inline--fa.fa-pull-left {
  margin-right: var(--fa-pull-margin, 0.3em);
  width: auto;
}
.svg-inline--fa.fa-pull-right {
  margin-left: var(--fa-pull-margin, 0.3em);
  width: auto;
}
.svg-inline--fa.fa-li {
  width: var(--fa-li-width, 2em);
  top: 0.25em;
}
.svg-inline--fa.fa-fw {
  width: var(--fa-fw-width, 1.25em);
}

.fa-layers svg.svg-inline--fa {
  bottom: 0;
  left: 0;
  margin: auto;
  position: absolute;
  right: 0;
  top: 0;
}

.fa-layers-counter, .fa-layers-text {
  display: inline-block;
  position: absolute;
  text-align: center;
}

.fa-layers {
  display: inline-block;
  height: 1em;
  position: relative;
  text-align: center;
  vertical-align: -0.125em;
  width: 1em;
}
.fa-layers svg.svg-inline--fa {
  -webkit-transform-origin: center center;
          transform-origin: center center;
}

.fa-layers-text {
  left: 50%;
  top: 50%;
  -webkit-transform: translate(-50%, -50%);
          transform: translate(-50%, -50%);
  -webkit-transform-origin: center center;
          transform-origin: center center;
}

.fa-layers-counter {
  background-color: var(--fa-counter-background-color, #ff253a);
  border-radius: var(--fa-counter-border-radius, 1em);
  box-sizing: border-box;
  color: var(--fa-inverse, #fff);
  line-height: var(--fa-counter-line-height, 1);
  max-width: var(--fa-counter-max-width, 5em);
  min-width: var(--fa-counter-min-width, 1.5em);
  overflow: hidden;
  padding: var(--fa-counter-padding, 0.25em 0.5em);
  right: var(--fa-right, 0);
  text-overflow: ellipsis;
  top: var(--fa-top, 0);
  -webkit-transform: scale(var(--fa-counter-scale, 0.25));
          transform: scale(var(--fa-counter-scale, 0.25));
  -webkit-transform-origin: top right;
          transform-origin: top right;
}

.fa-layers-bottom-right {
  bottom: var(--fa-bottom, 0);
  right: var(--fa-right, 0);
  top: auto;
  -webkit-transform: scale(var(--fa-layers-scale, 0.25));
          transform: scale(var(--fa-layers-scale, 0.25));
  -webkit-transform-origin: bottom right;
          transform-origin: bottom right;
}

.fa-layers-bottom-left {
  bottom: var(--fa-bottom, 0);
  left: var(--fa-left, 0);
  right: auto;
  top: auto;
  -webkit-transform: scale(var(--fa-layers-scale, 0.25));
          transform: scale(var(--fa-layers-scale, 0.25));
  -webkit-transform-origin: bottom left;
          transform-origin: bottom left;
}

.fa-layers-top-right {
  top: var(--fa-top, 0);
  right: var(--fa-right, 0);
  -webkit-transform: scale(var(--fa-layers-scale, 0.25));
          transform: scale(var(--fa-layers-scale, 0.25));
  -webkit-transform-origin: top right;
          transform-origin: top right;
}

.fa-layers-top-left {
  left: var(--fa-left, 0);
  right: auto;
  top: var(--fa-top, 0);
  -webkit-transform: scale(var(--fa-layers-scale, 0.25));
          transform: scale(var(--fa-layers-scale, 0.25));
  -webkit-transform-origin: top left;
          transform-origin: top left;
}

.fa-1x {
  font-size: 1em;
}

.fa-2x {
  font-size: 2em;
}

.fa-3x {
  font-size: 3em;
}

.fa-4x {
  font-size: 4em;
}

.fa-5x {
  font-size: 5em;
}

.fa-6x {
  font-size: 6em;
}

.fa-7x {
  font-size: 7em;
}

.fa-8x {
  font-size: 8em;
}

.fa-9x {
  font-size: 9em;
}

.fa-10x {
  font-size: 10em;
}

.fa-2xs {
  font-size: 0.625em;
  line-height: 0.1em;
  vertical-align: 0.225em;
}

.fa-xs {
  font-size: 0.75em;
  line-height: 0.0833333337em;
  vertical-align: 0.125em;
}

.fa-sm {
  font-size: 0.875em;
  line-height: 0.0714285718em;
  vertical-align: 0.0535714295em;
}

.fa-lg {
  font-size: 1.25em;
  line-height: 0.05em;
  vertical-align: -0.075em;
}

.fa-xl {
  font-size: 1.5em;
  line-height: 0.0416666682em;
  vertical-align: -0.125em;
}

.fa-2xl {
  font-size: 2em;
  line-height: 0.03125em;
  vertical-align: -0.1875em;
}

.fa-fw {
  text-align: center;
  width: 1.25em;
}

.fa-ul {
  list-style-type: none;
  margin-left: var(--fa-li-margin, 2.5em);
  padding-left: 0;
}
.fa-ul > li {
  position: relative;
}

.fa-li {
  left: calc(var(--fa-li-width, 2em) * -1);
  position: absolute;
  text-align: center;
  width: var(--fa-li-width, 2em);
  line-height: inherit;
}

.fa-border {
  border-color: var(--fa-border-color, #eee);
  border-radius: var(--fa-border-radius, 0.1em);
  border-style: var(--fa-border-style, solid);
  border-width: var(--fa-border-width, 0.08em);
  padding: var(--fa-border-padding, 0.2em 0.25em 0.15em);
}

.fa-pull-left {
  float: left;
  margin-right: var(--fa-pull-margin, 0.3em);
}

.fa-pull-right {
  float: right;
  margin-left: var(--fa-pull-margin, 0.3em);
}

.fa-beat {
  -webkit-animation-name: fa-beat;
          animation-name: fa-beat;
  -webkit-animation-delay: var(--fa-animation-delay, 0);
          animation-delay: var(--fa-animation-delay, 0);
  -webkit-animation-direction: var(--fa-animation-direction, normal);
          animation-direction: var(--fa-animation-direction, normal);
  -webkit-animation-duration: var(--fa-animation-duration, 1s);
          animation-duration: var(--fa-animation-duration, 1s);
  -webkit-animation-iteration-count: var(--fa-animation-iteration-count, infinite);
          animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  -webkit-animation-timing-function: var(--fa-animation-timing, ease-in-out);
          animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-bounce {
  -webkit-animation-name: fa-bounce;
          animation-name: fa-bounce;
  -webkit-animation-delay: var(--fa-animation-delay, 0);
          animation-delay: var(--fa-animation-delay, 0);
  -webkit-animation-direction: var(--fa-animation-direction, normal);
          animation-direction: var(--fa-animation-direction, normal);
  -webkit-animation-duration: var(--fa-animation-duration, 1s);
          animation-duration: var(--fa-animation-duration, 1s);
  -webkit-animation-iteration-count: var(--fa-animation-iteration-count, infinite);
          animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  -webkit-animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.28, 0.84, 0.42, 1));
          animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.28, 0.84, 0.42, 1));
}

.fa-fade {
  -webkit-animation-name: fa-fade;
          animation-name: fa-fade;
  -webkit-animation-delay: var(--fa-animation-delay, 0);
          animation-delay: var(--fa-animation-delay, 0);
  -webkit-animation-direction: var(--fa-animation-direction, normal);
          animation-direction: var(--fa-animation-direction, normal);
  -webkit-animation-duration: var(--fa-animation-duration, 1s);
          animation-duration: var(--fa-animation-duration, 1s);
  -webkit-animation-iteration-count: var(--fa-animation-iteration-count, infinite);
          animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  -webkit-animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
          animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-beat-fade {
  -webkit-animation-name: fa-beat-fade;
          animation-name: fa-beat-fade;
  -webkit-animation-delay: var(--fa-animation-delay, 0);
          animation-delay: var(--fa-animation-delay, 0);
  -webkit-animation-direction: var(--fa-animation-direction, normal);
          animation-direction: var(--fa-animation-direction, normal);
  -webkit-animation-duration: var(--fa-animation-duration, 1s);
          animation-duration: var(--fa-animation-duration, 1s);
  -webkit-animation-iteration-count: var(--fa-animation-iteration-count, infinite);
          animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  -webkit-animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
          animation-timing-function: var(--fa-animation-timing, cubic-bezier(0.4, 0, 0.6, 1));
}

.fa-flip {
  -webkit-animation-name: fa-flip;
          animation-name: fa-flip;
  -webkit-animation-delay: var(--fa-animation-delay, 0);
          animation-delay: var(--fa-animation-delay, 0);
  -webkit-animation-direction: var(--fa-animation-direction, normal);
          animation-direction: var(--fa-animation-direction, normal);
  -webkit-animation-duration: var(--fa-animation-duration, 1s);
          animation-duration: var(--fa-animation-duration, 1s);
  -webkit-animation-iteration-count: var(--fa-animation-iteration-count, infinite);
          animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  -webkit-animation-timing-function: var(--fa-animation-timing, ease-in-out);
          animation-timing-function: var(--fa-animation-timing, ease-in-out);
}

.fa-shake {
  -webkit-animation-name: fa-shake;
          animation-name: fa-shake;
  -webkit-animation-delay: var(--fa-animation-delay, 0);
          animation-delay: var(--fa-animation-delay, 0);
  -webkit-animation-direction: var(--fa-animation-direction, normal);
          animation-direction: var(--fa-animation-direction, normal);
  -webkit-animation-duration: var(--fa-animation-duration, 1s);
          animation-duration: var(--fa-animation-duration, 1s);
  -webkit-animation-iteration-count: var(--fa-animation-iteration-count, infinite);
          animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  -webkit-animation-timing-function: var(--fa-animation-timing, linear);
          animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin {
  -webkit-animation-name: fa-spin;
          animation-name: fa-spin;
  -webkit-animation-delay: var(--fa-animation-delay, 0);
          animation-delay: var(--fa-animation-delay, 0);
  -webkit-animation-direction: var(--fa-animation-direction, normal);
          animation-direction: var(--fa-animation-direction, normal);
  -webkit-animation-duration: var(--fa-animation-duration, 2s);
          animation-duration: var(--fa-animation-duration, 2s);
  -webkit-animation-iteration-count: var(--fa-animation-iteration-count, infinite);
          animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  -webkit-animation-timing-function: var(--fa-animation-timing, linear);
          animation-timing-function: var(--fa-animation-timing, linear);
}

.fa-spin-reverse {
  --fa-animation-direction: reverse;
}

.fa-pulse,
.fa-spin-pulse {
  -webkit-animation-name: fa-spin;
          animation-name: fa-spin;
  -webkit-animation-direction: var(--fa-animation-direction, normal);
          animation-direction: var(--fa-animation-direction, normal);
  -webkit-animation-duration: var(--fa-animation-duration, 1s);
          animation-duration: var(--fa-animation-duration, 1s);
  -webkit-animation-iteration-count: var(--fa-animation-iteration-count, infinite);
          animation-iteration-count: var(--fa-animation-iteration-count, infinite);
  -webkit-animation-timing-function: var(--fa-animation-timing, steps(8));
          animation-timing-function: var(--fa-animation-timing, steps(8));
}

@media (prefers-reduced-motion: reduce) {
  .fa-beat,
.fa-bounce,
.fa-fade,
.fa-beat-fade,
.fa-flip,
.fa-pulse,
.fa-shake,
.fa-spin,
.fa-spin-pulse {
    -webkit-animation-delay: -1ms;
            animation-delay: -1ms;
    -webkit-animation-duration: 1ms;
            animation-duration: 1ms;
    -webkit-animation-iteration-count: 1;
            animation-iteration-count: 1;
    transition-delay: 0s;
    transition-duration: 0s;
  }
}
@-webkit-keyframes fa-beat {
  0%, 90% {
    -webkit-transform: scale(1);
            transform: scale(1);
  }
  45% {
    -webkit-transform: scale(var(--fa-beat-scale, 1.25));
            transform: scale(var(--fa-beat-scale, 1.25));
  }
}
@keyframes fa-beat {
  0%, 90% {
    -webkit-transform: scale(1);
            transform: scale(1);
  }
  45% {
    -webkit-transform: scale(var(--fa-beat-scale, 1.25));
            transform: scale(var(--fa-beat-scale, 1.25));
  }
}
@-webkit-keyframes fa-bounce {
  0% {
    -webkit-transform: scale(1, 1) translateY(0);
            transform: scale(1, 1) translateY(0);
  }
  10% {
    -webkit-transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);
            transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);
  }
  30% {
    -webkit-transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));
            transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));
  }
  50% {
    -webkit-transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);
            transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);
  }
  57% {
    -webkit-transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));
            transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));
  }
  64% {
    -webkit-transform: scale(1, 1) translateY(0);
            transform: scale(1, 1) translateY(0);
  }
  100% {
    -webkit-transform: scale(1, 1) translateY(0);
            transform: scale(1, 1) translateY(0);
  }
}
@keyframes fa-bounce {
  0% {
    -webkit-transform: scale(1, 1) translateY(0);
            transform: scale(1, 1) translateY(0);
  }
  10% {
    -webkit-transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);
            transform: scale(var(--fa-bounce-start-scale-x, 1.1), var(--fa-bounce-start-scale-y, 0.9)) translateY(0);
  }
  30% {
    -webkit-transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));
            transform: scale(var(--fa-bounce-jump-scale-x, 0.9), var(--fa-bounce-jump-scale-y, 1.1)) translateY(var(--fa-bounce-height, -0.5em));
  }
  50% {
    -webkit-transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);
            transform: scale(var(--fa-bounce-land-scale-x, 1.05), var(--fa-bounce-land-scale-y, 0.95)) translateY(0);
  }
  57% {
    -webkit-transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));
            transform: scale(1, 1) translateY(var(--fa-bounce-rebound, -0.125em));
  }
  64% {
    -webkit-transform: scale(1, 1) translateY(0);
            transform: scale(1, 1) translateY(0);
  }
  100% {
    -webkit-transform: scale(1, 1) translateY(0);
            transform: scale(1, 1) translateY(0);
  }
}
@-webkit-keyframes fa-fade {
  50% {
    opacity: var(--fa-fade-opacity, 0.4);
  }
}
@keyframes fa-fade {
  50% {
    opacity: var(--fa-fade-opacity, 0.4);
  }
}
@-webkit-keyframes fa-beat-fade {
  0%, 100% {
    opacity: var(--fa-beat-fade-opacity, 0.4);
    -webkit-transform: scale(1);
            transform: scale(1);
  }
  50% {
    opacity: 1;
    -webkit-transform: scale(var(--fa-beat-fade-scale, 1.125));
            transform: scale(var(--fa-beat-fade-scale, 1.125));
  }
}
@keyframes fa-beat-fade {
  0%, 100% {
    opacity: var(--fa-beat-fade-opacity, 0.4);
    -webkit-transform: scale(1);
            transform: scale(1);
  }
  50% {
    opacity: 1;
    -webkit-transform: scale(var(--fa-beat-fade-scale, 1.125));
            transform: scale(var(--fa-beat-fade-scale, 1.125));
  }
}
@-webkit-keyframes fa-flip {
  50% {
    -webkit-transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));
            transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));
  }
}
@keyframes fa-flip {
  50% {
    -webkit-transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));
            transform: rotate3d(var(--fa-flip-x, 0), var(--fa-flip-y, 1), var(--fa-flip-z, 0), var(--fa-flip-angle, -180deg));
  }
}
@-webkit-keyframes fa-shake {
  0% {
    -webkit-transform: rotate(-15deg);
            transform: rotate(-15deg);
  }
  4% {
    -webkit-transform: rotate(15deg);
            transform: rotate(15deg);
  }
  8%, 24% {
    -webkit-transform: rotate(-18deg);
            transform: rotate(-18deg);
  }
  12%, 28% {
    -webkit-transform: rotate(18deg);
            transform: rotate(18deg);
  }
  16% {
    -webkit-transform: rotate(-22deg);
            transform: rotate(-22deg);
  }
  20% {
    -webkit-transform: rotate(22deg);
            transform: rotate(22deg);
  }
  32% {
    -webkit-transform: rotate(-12deg);
            transform: rotate(-12deg);
  }
  36% {
    -webkit-transform: rotate(12deg);
            transform: rotate(12deg);
  }
  40%, 100% {
    -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
  }
}
@keyframes fa-shake {
  0% {
    -webkit-transform: rotate(-15deg);
            transform: rotate(-15deg);
  }
  4% {
    -webkit-transform: rotate(15deg);
            transform: rotate(15deg);
  }
  8%, 24% {
    -webkit-transform: rotate(-18deg);
            transform: rotate(-18deg);
  }
  12%, 28% {
    -webkit-transform: rotate(18deg);
            transform: rotate(18deg);
  }
  16% {
    -webkit-transform: rotate(-22deg);
            transform: rotate(-22deg);
  }
  20% {
    -webkit-transform: rotate(22deg);
            transform: rotate(22deg);
  }
  32% {
    -webkit-transform: rotate(-12deg);
            transform: rotate(-12deg);
  }
  36% {
    -webkit-transform: rotate(12deg);
            transform: rotate(12deg);
  }
  40%, 100% {
    -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
  }
}
@-webkit-keyframes fa-spin {
  0% {
    -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
  }
}
@keyframes fa-spin {
  0% {
    -webkit-transform: rotate(0deg);
            transform: rotate(0deg);
  }
  100% {
    -webkit-transform: rotate(360deg);
            transform: rotate(360deg);
  }
}
.fa-rotate-90 {
  -webkit-transform: rotate(90deg);
          transform: rotate(90deg);
}

.fa-rotate-180 {
  -webkit-transform: rotate(180deg);
          transform: rotate(180deg);
}

.fa-rotate-270 {
  -webkit-transform: rotate(270deg);
          transform: rotate(270deg);
}

.fa-flip-horizontal {
  -webkit-transform: scale(-1, 1);
          transform: scale(-1, 1);
}

.fa-flip-vertical {
  -webkit-transform: scale(1, -1);
          transform: scale(1, -1);
}

.fa-flip-both,
.fa-flip-horizontal.fa-flip-vertical {
  -webkit-transform: scale(-1, -1);
          transform: scale(-1, -1);
}

.fa-rotate-by {
  -webkit-transform: rotate(var(--fa-rotate-angle, none));
          transform: rotate(var(--fa-rotate-angle, none));
}

.fa-stack {
  display: inline-block;
  vertical-align: middle;
  height: 2em;
  position: relative;
  width: 2.5em;
}

.fa-stack-1x,
.fa-stack-2x {
  bottom: 0;
  left: 0;
  margin: auto;
  position: absolute;
  right: 0;
  top: 0;
  z-index: var(--fa-stack-z-index, auto);
}

.svg-inline--fa.fa-stack-1x {
  height: 1em;
  width: 1.25em;
}
.svg-inline--fa.fa-stack-2x {
  height: 2em;
  width: 2.5em;
}

.fa-inverse {
  color: var(--fa-inverse, #fff);
}

.sr-only,
.fa-sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.sr-only-focusable:not(:focus),
.fa-sr-only-focusable:not(:focus) {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border-width: 0;
}

.svg-inline--fa .fa-primary {
  fill: var(--fa-primary-color, currentColor);
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa .fa-secondary {
  fill: var(--fa-secondary-color, currentColor);
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-primary {
  opacity: var(--fa-secondary-opacity, 0.4);
}

.svg-inline--fa.fa-swap-opacity .fa-secondary {
  opacity: var(--fa-primary-opacity, 1);
}

.svg-inline--fa mask .fa-primary,
.svg-inline--fa mask .fa-secondary {
  fill: black;
}

.fad.fa-inverse,
.fa-duotone.fa-inverse {
  color: var(--fa-inverse, #fff);
}`;function ha(){var t=fa,e=ua,n=b.familyPrefix,a=b.replacementClass,r=Qr;if(n!==t||a!==e){var i=new RegExp("\\.".concat(t,"\\-"),"g"),o=new RegExp("\\--".concat(t,"\\-"),"g"),s=new RegExp("\\.".concat(e),"g");r=r.replace(i,".".concat(n,"-")).replace(o,"--".concat(n,"-")).replace(s,".".concat(a))}return r}var bn=!1;function fe(){b.autoAddCss&&!bn&&(Gr(ha()),bn=!0)}var Zr={mixout:function(){return{dom:{css:ha,insertCss:fe}}},hooks:function(){return{beforeDOMElementCreation:function(){fe()},beforeI2svg:function(){fe()}}}},J=rt||{};J[K]||(J[K]={});J[K].styles||(J[K].styles={});J[K].hooks||(J[K].hooks={});J[K].shims||(J[K].shims=[]);var Y=J[K],ga=[],ti=function t(){S.removeEventListener("DOMContentLoaded",t),Ht=1,ga.map(function(e){return e()})},Ht=!1;Z&&(Ht=(S.documentElement.doScroll?/^loaded|^c/:/^loaded|^i|^c/).test(S.readyState),Ht||S.addEventListener("DOMContentLoaded",ti));function ei(t){!Z||(Ht?setTimeout(t,0):ga.push(t))}function $t(t){var e=t.tag,n=t.attributes,a=n===void 0?{}:n,r=t.children,i=r===void 0?[]:r;return typeof t=="string"?ba(t):"<".concat(e," ").concat(qr(a),">").concat(i.map($t).join(""),"</").concat(e,">")}function hn(t,e,n){if(t&&t[e]&&t[e][n])return{prefix:e,iconName:n,icon:t[e][n]}}var ni=function(e,n){return function(a,r,i,o){return e.call(n,a,r,i,o)}},ue=function(e,n,a,r){var i=Object.keys(e),o=i.length,s=r!==void 0?ni(n,r):n,l,f,u;for(a===void 0?(l=1,u=e[i[0]]):(l=0,u=a);l<o;l++)f=i[l],u=s(u,e[f],f,e);return u};function ai(t){for(var e=[],n=0,a=t.length;n<a;){var r=t.charCodeAt(n++);if(r>=55296&&r<=56319&&n<a){var i=t.charCodeAt(n++);(i&64512)==56320?e.push(((r&1023)<<10)+(i&1023)+65536):(e.push(r),n--)}else e.push(r)}return e}function Ce(t){var e=ai(t);return e.length===1?e[0].toString(16):null}function ri(t,e){var n=t.length,a=t.charCodeAt(e),r;return a>=55296&&a<=56319&&n>e+1&&(r=t.charCodeAt(e+1),r>=56320&&r<=57343)?(a-55296)*1024+r-56320+65536:a}function gn(t){return Object.keys(t).reduce(function(e,n){var a=t[n],r=!!a.icon;return r?e[a.iconName]=a.icon:e[n]=a,e},{})}function Ae(t,e){var n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{},a=n.skipHooks,r=a===void 0?!1:a,i=gn(e);typeof Y.hooks.addPack=="function"&&!r?Y.hooks.addPack(t,gn(e)):Y.styles[t]=d(d({},Y.styles[t]||{}),i),t==="fas"&&Ae("fa",e)}var Rt=Y.styles,ii=Y.shims,oi=Object.values(da),Be=null,ya={},wa={},xa={},ka={},Ca={},si=Object.keys(Ue);function li(t){return~Wr.indexOf(t)}function fi(t,e){var n=e.split("-"),a=n[0],r=n.slice(1).join("-");return a===t&&r!==""&&!li(r)?r:null}var Aa=function(){var e=function(i){return ue(Rt,function(o,s,l){return o[l]=ue(s,i,{}),o},{})};ya=e(function(r,i,o){if(i[3]&&(r[i[3]]=o),i[2]){var s=i[2].filter(function(l){return typeof l=="number"});s.forEach(function(l){r[l.toString(16)]=o})}return r}),wa=e(function(r,i,o){if(r[o]=o,i[2]){var s=i[2].filter(function(l){return typeof l=="string"});s.forEach(function(l){r[l]=o})}return r}),Ca=e(function(r,i,o){var s=i[2];return r[o]=o,s.forEach(function(l){r[l]=o}),r});var n="far"in Rt||b.autoFetchSvg,a=ue(ii,function(r,i){var o=i[0],s=i[1],l=i[2];return s==="far"&&!n&&(s="fas"),typeof o=="string"&&(r.names[o]={prefix:s,iconName:l}),typeof o=="number"&&(r.unicodes[o.toString(16)]={prefix:s,iconName:l}),r},{names:{},unicodes:{}});xa=a.names,ka=a.unicodes,Be=Jt(b.styleDefault)};Br(function(t){Be=Jt(t.styleDefault)});Aa();function Ge(t,e){return(ya[t]||{})[e]}function ui(t,e){return(wa[t]||{})[e]}function bt(t,e){return(Ca[t]||{})[e]}function Oa(t){return xa[t]||{prefix:null,iconName:null}}function ci(t){var e=ka[t],n=Ge("fas",t);return e||(n?{prefix:"fas",iconName:n}:null)||{prefix:null,iconName:null}}function it(){return Be}var Xe=function(){return{prefix:null,iconName:null,rest:[]}};function Jt(t){var e=Ue[t],n=Vt[t]||Vt[e],a=t in Y.styles?t:null;return n||a||null}function Qt(t){var e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=e.skipLookups,a=n===void 0?!1:n,r=null,i=t.reduce(function(o,s){var l=fi(b.familyPrefix,s);if(Rt[s]?(s=oi.includes(s)?Mr[s]:s,r=s,o.prefix=s):si.indexOf(s)>-1?(r=s,o.prefix=Jt(s)):l?o.iconName=l:s!==b.replacementClass&&o.rest.push(s),!a&&o.prefix&&o.iconName){var f=r==="fa"?Oa(o.iconName):{},u=bt(o.prefix,o.iconName);f.prefix&&(r=null),o.iconName=f.iconName||u||o.iconName,o.prefix=f.prefix||o.prefix,o.prefix==="far"&&!Rt.far&&Rt.fas&&!b.autoFetchSvg&&(o.prefix="fas")}return o},Xe());return(i.prefix==="fa"||r==="fa")&&(i.prefix=it()||"fas"),i}var di=function(){function t(){kr(this,t),this.definitions={}}return Cr(t,[{key:"add",value:function(){for(var n=this,a=arguments.length,r=new Array(a),i=0;i<a;i++)r[i]=arguments[i];var o=r.reduce(this._pullDefinitions,{});Object.keys(o).forEach(function(s){n.definitions[s]=d(d({},n.definitions[s]||{}),o[s]),Ae(s,o[s]);var l=da[s];l&&Ae(l,o[s]),Aa()})}},{key:"reset",value:function(){this.definitions={}}},{key:"_pullDefinitions",value:function(n,a){var r=a.prefix&&a.iconName&&a.icon?{0:a}:a;return Object.keys(r).map(function(i){var o=r[i],s=o.prefix,l=o.iconName,f=o.icon,u=f[2];n[s]||(n[s]={}),u.length>0&&u.forEach(function(c){typeof c=="string"&&(n[s][c]=f)}),n[s][l]=f}),n}}]),t}(),yn=[],ht={},yt={},mi=Object.keys(yt);function vi(t,e){var n=e.mixoutsTo;return yn=t,ht={},Object.keys(yt).forEach(function(a){mi.indexOf(a)===-1&&delete yt[a]}),yn.forEach(function(a){var r=a.mixout?a.mixout():{};if(Object.keys(r).forEach(function(o){typeof r[o]=="function"&&(n[o]=r[o]),Ut(r[o])==="object"&&Object.keys(r[o]).forEach(function(s){n[o]||(n[o]={}),n[o][s]=r[o][s]})}),a.hooks){var i=a.hooks();Object.keys(i).forEach(function(o){ht[o]||(ht[o]=[]),ht[o].push(i[o])})}a.provides&&a.provides(yt)}),n}function Oe(t,e){for(var n=arguments.length,a=new Array(n>2?n-2:0),r=2;r<n;r++)a[r-2]=arguments[r];var i=ht[t]||[];return i.forEach(function(o){e=o.apply(null,[e].concat(a))}),e}function dt(t){for(var e=arguments.length,n=new Array(e>1?e-1:0),a=1;a<e;a++)n[a-1]=arguments[a];var r=ht[t]||[];r.forEach(function(i){i.apply(null,n)})}function Q(){var t=arguments[0],e=Array.prototype.slice.call(arguments,1);return yt[t]?yt[t].apply(null,e):void 0}function Se(t){t.prefix==="fa"&&(t.prefix="fas");var e=t.iconName,n=t.prefix||it();if(!!e)return e=bt(n,e)||e,hn(Sa.definitions,n,e)||hn(Y.styles,n,e)}var Sa=new di,pi=function(){b.autoReplaceSvg=!1,b.observeMutations=!1,dt("noAuto")},bi={i2svg:function(){var e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};return Z?(dt("beforeI2svg",e),Q("pseudoElements2svg",e),Q("i2svg",e)):Promise.reject("Operation requires a DOM of some kind.")},watch:function(){var e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},n=e.autoReplaceSvgRoot;b.autoReplaceSvg===!1&&(b.autoReplaceSvg=!0),b.observeMutations=!0,ei(function(){gi({autoReplaceSvgRoot:n}),dt("watch",e)})}},hi={icon:function(e){if(e===null)return null;if(Ut(e)==="object"&&e.prefix&&e.iconName)return{prefix:e.prefix,iconName:bt(e.prefix,e.iconName)||e.iconName};if(Array.isArray(e)&&e.length===2){var n=e[1].indexOf("fa-")===0?e[1].slice(3):e[1],a=Jt(e[0]);return{prefix:a,iconName:bt(a,n)||n}}if(typeof e=="string"&&(e.indexOf("".concat(b.familyPrefix,"-"))>-1||e.match(Lr))){var r=Qt(e.split(" "),{skipLookups:!0});return{prefix:r.prefix||it(),iconName:bt(r.prefix,r.iconName)||r.iconName}}if(typeof e=="string"){var i=it();return{prefix:i,iconName:bt(i,e)||e}}}},D={noAuto:pi,config:b,dom:bi,parse:hi,library:Sa,findIconDefinition:Se,toHtml:$t},gi=function(){var e=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{},n=e.autoReplaceSvgRoot,a=n===void 0?S:n;(Object.keys(Y.styles).length>0||b.autoFetchSvg)&&Z&&b.autoReplaceSvg&&D.dom.i2svg({node:a})};function Zt(t,e){return Object.defineProperty(t,"abstract",{get:e}),Object.defineProperty(t,"html",{get:function(){return t.abstract.map(function(a){return $t(a)})}}),Object.defineProperty(t,"node",{get:function(){if(!!Z){var a=S.createElement("div");return a.innerHTML=t.html,a.children}}}),t}function yi(t){var e=t.children,n=t.main,a=t.mask,r=t.attributes,i=t.styles,o=t.transform;if(He(o)&&n.found&&!a.found){var s=n.width,l=n.height,f={x:s/l/2,y:.5};r.style=Kt(d(d({},i),{},{"transform-origin":"".concat(f.x+o.x/16,"em ").concat(f.y+o.y/16,"em")}))}return[{tag:"svg",attributes:r,children:e}]}function wi(t){var e=t.prefix,n=t.iconName,a=t.children,r=t.attributes,i=t.symbol,o=i===!0?"".concat(e,"-").concat(b.familyPrefix,"-").concat(n):i;return[{tag:"svg",attributes:{style:"display: none;"},children:[{tag:"symbol",attributes:d(d({},r),{},{id:o}),children:a}]}]}function qe(t){var e=t.icons,n=e.main,a=e.mask,r=t.prefix,i=t.iconName,o=t.transform,s=t.symbol,l=t.title,f=t.maskId,u=t.titleId,c=t.extra,v=t.watchable,g=v===void 0?!1:v,O=a.found?a:n,x=O.width,h=O.height,m=r==="fak",A=[b.replacementClass,i?"".concat(b.familyPrefix,"-").concat(i):""].filter(function(E){return c.classes.indexOf(E)===-1}).filter(function(E){return E!==""||!!E}).concat(c.classes).join(" "),k={children:[],attributes:d(d({},c.attributes),{},{"data-prefix":r,"data-icon":i,class:A,role:c.attributes.role||"img",xmlns:"http://www.w3.org/2000/svg",viewBox:"0 0 ".concat(x," ").concat(h)})},T=m&&!~c.classes.indexOf("fa-fw")?{width:"".concat(x/h*16*.0625,"em")}:{};g&&(k.attributes[ct]=""),l&&(k.children.push({tag:"title",attributes:{id:k.attributes["aria-labelledby"]||"title-".concat(u||_t())},children:[l]}),delete k.attributes.title);var w=d(d({},k),{},{prefix:r,iconName:i,main:n,mask:a,maskId:f,transform:o,symbol:s,styles:d(d({},T),c.styles)}),R=a.found&&n.found?Q("generateAbstractMask",w)||{children:[],attributes:{}}:Q("generateAbstractIcon",w)||{children:[],attributes:{}},M=R.children,L=R.attributes;return w.children=M,w.attributes=L,s?wi(w):yi(w)}function wn(t){var e=t.content,n=t.width,a=t.height,r=t.transform,i=t.title,o=t.extra,s=t.watchable,l=s===void 0?!1:s,f=d(d(d({},o.attributes),i?{title:i}:{}),{},{class:o.classes.join(" ")});l&&(f[ct]="");var u=d({},o.styles);He(r)&&(u.transform=Jr({transform:r,startCentered:!0,width:n,height:a}),u["-webkit-transform"]=u.transform);var c=Kt(u);c.length>0&&(f.style=c);var v=[];return v.push({tag:"span",attributes:f,children:[e]}),i&&v.push({tag:"span",attributes:{class:"sr-only"},children:[i]}),v}function xi(t){var e=t.content,n=t.title,a=t.extra,r=d(d(d({},a.attributes),n?{title:n}:{}),{},{class:a.classes.join(" ")}),i=Kt(a.styles);i.length>0&&(r.style=i);var o=[];return o.push({tag:"span",attributes:r,children:[e]}),n&&o.push({tag:"span",attributes:{class:"sr-only"},children:[n]}),o}var ce=Y.styles;function Ee(t){var e=t[0],n=t[1],a=t.slice(4),r=je(a,1),i=r[0],o=null;return Array.isArray(i)?o={tag:"g",attributes:{class:"".concat(b.familyPrefix,"-").concat(ft.GROUP)},children:[{tag:"path",attributes:{class:"".concat(b.familyPrefix,"-").concat(ft.SECONDARY),fill:"currentColor",d:i[0]}},{tag:"path",attributes:{class:"".concat(b.familyPrefix,"-").concat(ft.PRIMARY),fill:"currentColor",d:i[1]}}]}:o={tag:"path",attributes:{fill:"currentColor",d:i}},{found:!0,width:e,height:n,icon:o}}var ki={found:!1,width:512,height:512};function Ci(t,e){!ca&&!b.showMissingIcons&&t&&console.error('Icon with name "'.concat(t,'" and prefix "').concat(e,'" is missing.'))}function Te(t,e){var n=e;return e==="fa"&&b.styleDefault!==null&&(e=it()),new Promise(function(a,r){if(Q("missingIconAbstract"),n==="fa"){var i=Oa(t)||{};t=i.iconName||t,e=i.prefix||e}if(t&&e&&ce[e]&&ce[e][t]){var o=ce[e][t];return a(Ee(o))}Ci(t,e),a(d(d({},ki),{},{icon:b.showMissingIcons&&t?Q("missingIconAbstract")||{}:{}}))})}var xn=function(){},Ie=b.measurePerformance&&zt&&zt.mark&&zt.measure?zt:{mark:xn,measure:xn},St='FA "6.1.1"',Ai=function(e){return Ie.mark("".concat(St," ").concat(e," begins")),function(){return Ea(e)}},Ea=function(e){Ie.mark("".concat(St," ").concat(e," ends")),Ie.measure("".concat(St," ").concat(e),"".concat(St," ").concat(e," begins"),"".concat(St," ").concat(e," ends"))},Ke={begin:Ai,end:Ea},Ft=function(){};function kn(t){var e=t.getAttribute?t.getAttribute(ct):null;return typeof e=="string"}function Oi(t){var e=t.getAttribute?t.getAttribute(We):null,n=t.getAttribute?t.getAttribute(Ye):null;return e&&n}function Si(t){return t&&t.classList&&t.classList.contains&&t.classList.contains(b.replacementClass)}function Ei(){if(b.autoReplaceSvg===!0)return Wt.replace;var t=Wt[b.autoReplaceSvg];return t||Wt.replace}function Ti(t){return S.createElementNS("http://www.w3.org/2000/svg",t)}function Ii(t){return S.createElement(t)}function Ta(t){var e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},n=e.ceFn,a=n===void 0?t.tag==="svg"?Ti:Ii:n;if(typeof t=="string")return S.createTextNode(t);var r=a(t.tag);Object.keys(t.attributes||[]).forEach(function(o){r.setAttribute(o,t.attributes[o])});var i=t.children||[];return i.forEach(function(o){r.appendChild(Ta(o,{ceFn:a}))}),r}function Pi(t){var e=" ".concat(t.outerHTML," ");return e="".concat(e,"Font Awesome fontawesome.com "),e}var Wt={replace:function(e){var n=e[0];if(n.parentNode)if(e[1].forEach(function(r){n.parentNode.insertBefore(Ta(r),n)}),n.getAttribute(ct)===null&&b.keepOriginalSource){var a=S.createComment(Pi(n));n.parentNode.replaceChild(a,n)}else n.remove()},nest:function(e){var n=e[0],a=e[1];if(~Ve(n).indexOf(b.replacementClass))return Wt.replace(e);var r=new RegExp("".concat(b.familyPrefix,"-.*"));if(delete a[0].attributes.id,a[0].attributes.class){var i=a[0].attributes.class.split(" ").reduce(function(s,l){return l===b.replacementClass||l.match(r)?s.toSvg.push(l):s.toNode.push(l),s},{toNode:[],toSvg:[]});a[0].attributes.class=i.toSvg.join(" "),i.toNode.length===0?n.removeAttribute("class"):n.setAttribute("class",i.toNode.join(" "))}var o=a.map(function(s){return $t(s)}).join(`
`);n.setAttribute(ct,""),n.innerHTML=o}};function Cn(t){t()}function Ia(t,e){var n=typeof e=="function"?e:Ft;if(t.length===0)n();else{var a=Cn;b.mutateApproach===_r&&(a=rt.requestAnimationFrame||Cn),a(function(){var r=Ei(),i=Ke.begin("mutate");t.map(r),i(),n()})}}var Je=!1;function Pa(){Je=!0}function Pe(){Je=!1}var Bt=null;function An(t){if(!!vn&&!!b.observeMutations){var e=t.treeCallback,n=e===void 0?Ft:e,a=t.nodeCallback,r=a===void 0?Ft:a,i=t.pseudoElementsCallback,o=i===void 0?Ft:i,s=t.observeMutationsRoot,l=s===void 0?S:s;Bt=new vn(function(f){if(!Je){var u=it();wt(f).forEach(function(c){if(c.type==="childList"&&c.addedNodes.length>0&&!kn(c.addedNodes[0])&&(b.searchPseudoElements&&o(c.target),n(c.target)),c.type==="attributes"&&c.target.parentNode&&b.searchPseudoElements&&o(c.target.parentNode),c.type==="attributes"&&kn(c.target)&&~Fr.indexOf(c.attributeName))if(c.attributeName==="class"&&Oi(c.target)){var v=Qt(Ve(c.target)),g=v.prefix,O=v.iconName;c.target.setAttribute(We,g||u),O&&c.target.setAttribute(Ye,O)}else Si(c.target)&&r(c.target)})}}),Z&&Bt.observe(l,{childList:!0,attributes:!0,characterData:!0,subtree:!0})}}function Ri(){!Bt||Bt.disconnect()}function Ni(t){var e=t.getAttribute("style"),n=[];return e&&(n=e.split(";").reduce(function(a,r){var i=r.split(":"),o=i[0],s=i.slice(1);return o&&s.length>0&&(a[o]=s.join(":").trim()),a},{})),n}function _i(t){var e=t.getAttribute("data-prefix"),n=t.getAttribute("data-icon"),a=t.innerText!==void 0?t.innerText.trim():"",r=Qt(Ve(t));return r.prefix||(r.prefix=it()),e&&n&&(r.prefix=e,r.iconName=n),r.iconName&&r.prefix||r.prefix&&a.length>0&&(r.iconName=ui(r.prefix,t.innerText)||Ge(r.prefix,Ce(t.innerText))),r}function $i(t){var e=wt(t.attributes).reduce(function(r,i){return r.name!=="class"&&r.name!=="style"&&(r[i.name]=i.value),r},{}),n=t.getAttribute("title"),a=t.getAttribute("data-fa-title-id");return b.autoA11y&&(n?e["aria-labelledby"]="".concat(b.replacementClass,"-title-").concat(a||_t()):(e["aria-hidden"]="true",e.focusable="false")),e}function Mi(){return{iconName:null,title:null,titleId:null,prefix:null,transform:G,symbol:!1,mask:{iconName:null,prefix:null,rest:[]},maskId:null,extra:{classes:[],styles:{},attributes:{}}}}function On(t){var e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{styleParser:!0},n=_i(t),a=n.iconName,r=n.prefix,i=n.rest,o=$i(t),s=Oe("parseNodeAttributes",{},t),l=e.styleParser?Ni(t):[];return d({iconName:a,title:t.getAttribute("title"),titleId:t.getAttribute("data-fa-title-id"),prefix:r,transform:G,mask:{iconName:null,prefix:null,rest:[]},maskId:null,symbol:!1,extra:{classes:i,styles:l,attributes:o}},s)}var Li=Y.styles;function Ra(t){var e=b.autoReplaceSvg==="nest"?On(t,{styleParser:!1}):On(t);return~e.extra.classes.indexOf(ma)?Q("generateLayersText",t,e):Q("generateSvgReplacementMutation",t,e)}function Sn(t){var e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;if(!Z)return Promise.resolve();var n=S.documentElement.classList,a=function(c){return n.add("".concat(pn,"-").concat(c))},r=function(c){return n.remove("".concat(pn,"-").concat(c))},i=b.autoFetchSvg?Object.keys(Ue):Object.keys(Li),o=[".".concat(ma,":not([").concat(ct,"])")].concat(i.map(function(u){return".".concat(u,":not([").concat(ct,"])")})).join(", ");if(o.length===0)return Promise.resolve();var s=[];try{s=wt(t.querySelectorAll(o))}catch{}if(s.length>0)a("pending"),r("complete");else return Promise.resolve();var l=Ke.begin("onTree"),f=s.reduce(function(u,c){try{var v=Ra(c);v&&u.push(v)}catch(g){ca||g.name==="MissingIcon"&&console.error(g)}return u},[]);return new Promise(function(u,c){Promise.all(f).then(function(v){Ia(v,function(){a("active"),a("complete"),r("pending"),typeof e=="function"&&e(),l(),u()})}).catch(function(v){l(),c(v)})})}function Di(t){var e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:null;Ra(t).then(function(n){n&&Ia([n],e)})}function zi(t){return function(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=(e||{}).icon?e:Se(e||{}),r=n.mask;return r&&(r=(r||{}).icon?r:Se(r||{})),t(a,d(d({},n),{},{mask:r}))}}var ji=function(e){var n=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},a=n.transform,r=a===void 0?G:a,i=n.symbol,o=i===void 0?!1:i,s=n.mask,l=s===void 0?null:s,f=n.maskId,u=f===void 0?null:f,c=n.title,v=c===void 0?null:c,g=n.titleId,O=g===void 0?null:g,x=n.classes,h=x===void 0?[]:x,m=n.attributes,A=m===void 0?{}:m,k=n.styles,T=k===void 0?{}:k;if(!!e){var w=e.prefix,R=e.iconName,M=e.icon;return Zt(d({type:"icon"},e),function(){return dt("beforeDOMElementCreation",{iconDefinition:e,params:n}),b.autoA11y&&(v?A["aria-labelledby"]="".concat(b.replacementClass,"-title-").concat(O||_t()):(A["aria-hidden"]="true",A.focusable="false")),qe({icons:{main:Ee(M),mask:l?Ee(l.icon):{found:!1,width:null,height:null,icon:{}}},prefix:w,iconName:R,transform:d(d({},G),r),symbol:o,title:v,maskId:u,titleId:O,extra:{attributes:A,styles:T,classes:h}})})}},Fi={mixout:function(){return{icon:zi(ji)}},hooks:function(){return{mutationObserverCallbacks:function(n){return n.treeCallback=Sn,n.nodeCallback=Di,n}}},provides:function(e){e.i2svg=function(n){var a=n.node,r=a===void 0?S:a,i=n.callback,o=i===void 0?function(){}:i;return Sn(r,o)},e.generateSvgReplacementMutation=function(n,a){var r=a.iconName,i=a.title,o=a.titleId,s=a.prefix,l=a.transform,f=a.symbol,u=a.mask,c=a.maskId,v=a.extra;return new Promise(function(g,O){Promise.all([Te(r,s),u.iconName?Te(u.iconName,u.prefix):Promise.resolve({found:!1,width:512,height:512,icon:{}})]).then(function(x){var h=je(x,2),m=h[0],A=h[1];g([n,qe({icons:{main:m,mask:A},prefix:s,iconName:r,transform:l,symbol:f,maskId:c,title:i,titleId:o,extra:v,watchable:!0})])}).catch(O)})},e.generateAbstractIcon=function(n){var a=n.children,r=n.attributes,i=n.main,o=n.transform,s=n.styles,l=Kt(s);l.length>0&&(r.style=l);var f;return He(o)&&(f=Q("generateAbstractTransformGrouping",{main:i,transform:o,containerWidth:i.width,iconWidth:i.width})),a.push(f||i.icon),{children:a,attributes:r}}}},Wi={mixout:function(){return{layer:function(n){var a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=a.classes,i=r===void 0?[]:r;return Zt({type:"layer"},function(){dt("beforeDOMElementCreation",{assembler:n,params:a});var o=[];return n(function(s){Array.isArray(s)?s.map(function(l){o=o.concat(l.abstract)}):o=o.concat(s.abstract)}),[{tag:"span",attributes:{class:["".concat(b.familyPrefix,"-layers")].concat(qt(i)).join(" ")},children:o}]})}}}},Yi={mixout:function(){return{counter:function(n){var a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=a.title,i=r===void 0?null:r,o=a.classes,s=o===void 0?[]:o,l=a.attributes,f=l===void 0?{}:l,u=a.styles,c=u===void 0?{}:u;return Zt({type:"counter",content:n},function(){return dt("beforeDOMElementCreation",{content:n,params:a}),xi({content:n.toString(),title:i,extra:{attributes:f,styles:c,classes:["".concat(b.familyPrefix,"-layers-counter")].concat(qt(s))}})})}}}},Ui={mixout:function(){return{text:function(n){var a=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},r=a.transform,i=r===void 0?G:r,o=a.title,s=o===void 0?null:o,l=a.classes,f=l===void 0?[]:l,u=a.attributes,c=u===void 0?{}:u,v=a.styles,g=v===void 0?{}:v;return Zt({type:"text",content:n},function(){return dt("beforeDOMElementCreation",{content:n,params:a}),wn({content:n,transform:d(d({},G),i),title:s,extra:{attributes:c,styles:g,classes:["".concat(b.familyPrefix,"-layers-text")].concat(qt(f))}})})}}},provides:function(e){e.generateLayersText=function(n,a){var r=a.title,i=a.transform,o=a.extra,s=null,l=null;if(la){var f=parseInt(getComputedStyle(n).fontSize,10),u=n.getBoundingClientRect();s=u.width/f,l=u.height/f}return b.autoA11y&&!r&&(o.attributes["aria-hidden"]="true"),Promise.resolve([n,wn({content:n.innerHTML,width:s,height:l,transform:i,title:r,extra:o,watchable:!0})])}}},Vi=new RegExp('"',"ug"),En=[1105920,1112319];function Hi(t){var e=t.replace(Vi,""),n=ri(e,0),a=n>=En[0]&&n<=En[1],r=e.length===2?e[0]===e[1]:!1;return{value:Ce(r?e[0]:e),isSecondary:a||r}}function Tn(t,e){var n="".concat(Nr).concat(e.replace(":","-"));return new Promise(function(a,r){if(t.getAttribute(n)!==null)return a();var i=wt(t.children),o=i.filter(function(R){return R.getAttribute(ke)===e})[0],s=rt.getComputedStyle(t,e),l=s.getPropertyValue("font-family").match(Dr),f=s.getPropertyValue("font-weight"),u=s.getPropertyValue("content");if(o&&!l)return t.removeChild(o),a();if(l&&u!=="none"&&u!==""){var c=s.getPropertyValue("content"),v=~["Solid","Regular","Light","Thin","Duotone","Brands","Kit"].indexOf(l[2])?Vt[l[2].toLowerCase()]:zr[f],g=Hi(c),O=g.value,x=g.isSecondary,h=l[0].startsWith("FontAwesome"),m=Ge(v,O),A=m;if(h){var k=ci(O);k.iconName&&k.prefix&&(m=k.iconName,v=k.prefix)}if(m&&!x&&(!o||o.getAttribute(We)!==v||o.getAttribute(Ye)!==A)){t.setAttribute(n,A),o&&t.removeChild(o);var T=Mi(),w=T.extra;w.attributes[ke]=e,Te(m,v).then(function(R){var M=qe(d(d({},T),{},{icons:{main:R,mask:Xe()},prefix:v,iconName:A,extra:w,watchable:!0})),L=S.createElement("svg");e==="::before"?t.insertBefore(L,t.firstChild):t.appendChild(L),L.outerHTML=M.map(function(E){return $t(E)}).join(`
`),t.removeAttribute(n),a()}).catch(r)}else a()}else a()})}function Bi(t){return Promise.all([Tn(t,"::before"),Tn(t,"::after")])}function Gi(t){return t.parentNode!==document.head&&!~$r.indexOf(t.tagName.toUpperCase())&&!t.getAttribute(ke)&&(!t.parentNode||t.parentNode.tagName!=="svg")}function In(t){if(!!Z)return new Promise(function(e,n){var a=wt(t.querySelectorAll("*")).filter(Gi).map(Bi),r=Ke.begin("searchPseudoElements");Pa(),Promise.all(a).then(function(){r(),Pe(),e()}).catch(function(){r(),Pe(),n()})})}var Xi={hooks:function(){return{mutationObserverCallbacks:function(n){return n.pseudoElementsCallback=In,n}}},provides:function(e){e.pseudoElements2svg=function(n){var a=n.node,r=a===void 0?S:a;b.searchPseudoElements&&In(r)}}},Pn=!1,qi={mixout:function(){return{dom:{unwatch:function(){Pa(),Pn=!0}}}},hooks:function(){return{bootstrap:function(){An(Oe("mutationObserverCallbacks",{}))},noAuto:function(){Ri()},watch:function(n){var a=n.observeMutationsRoot;Pn?Pe():An(Oe("mutationObserverCallbacks",{observeMutationsRoot:a}))}}}},Rn=function(e){var n={size:16,x:0,y:0,flipX:!1,flipY:!1,rotate:0};return e.toLowerCase().split(" ").reduce(function(a,r){var i=r.toLowerCase().split("-"),o=i[0],s=i.slice(1).join("-");if(o&&s==="h")return a.flipX=!0,a;if(o&&s==="v")return a.flipY=!0,a;if(s=parseFloat(s),isNaN(s))return a;switch(o){case"grow":a.size=a.size+s;break;case"shrink":a.size=a.size-s;break;case"left":a.x=a.x-s;break;case"right":a.x=a.x+s;break;case"up":a.y=a.y-s;break;case"down":a.y=a.y+s;break;case"rotate":a.rotate=a.rotate+s;break}return a},n)},Ki={mixout:function(){return{parse:{transform:function(n){return Rn(n)}}}},hooks:function(){return{parseNodeAttributes:function(n,a){var r=a.getAttribute("data-fa-transform");return r&&(n.transform=Rn(r)),n}}},provides:function(e){e.generateAbstractTransformGrouping=function(n){var a=n.main,r=n.transform,i=n.containerWidth,o=n.iconWidth,s={transform:"translate(".concat(i/2," 256)")},l="translate(".concat(r.x*32,", ").concat(r.y*32,") "),f="scale(".concat(r.size/16*(r.flipX?-1:1),", ").concat(r.size/16*(r.flipY?-1:1),") "),u="rotate(".concat(r.rotate," 0 0)"),c={transform:"".concat(l," ").concat(f," ").concat(u)},v={transform:"translate(".concat(o/2*-1," -256)")},g={outer:s,inner:c,path:v};return{tag:"g",attributes:d({},g.outer),children:[{tag:"g",attributes:d({},g.inner),children:[{tag:a.icon.tag,children:a.icon.children,attributes:d(d({},a.icon.attributes),g.path)}]}]}}}},de={x:0,y:0,width:"100%",height:"100%"};function Nn(t){var e=arguments.length>1&&arguments[1]!==void 0?arguments[1]:!0;return t.attributes&&(t.attributes.fill||e)&&(t.attributes.fill="black"),t}function Ji(t){return t.tag==="g"?t.children:[t]}var Qi={hooks:function(){return{parseNodeAttributes:function(n,a){var r=a.getAttribute("data-fa-mask"),i=r?Qt(r.split(" ").map(function(o){return o.trim()})):Xe();return i.prefix||(i.prefix=it()),n.mask=i,n.maskId=a.getAttribute("data-fa-mask-id"),n}}},provides:function(e){e.generateAbstractMask=function(n){var a=n.children,r=n.attributes,i=n.main,o=n.mask,s=n.maskId,l=n.transform,f=i.width,u=i.icon,c=o.width,v=o.icon,g=Kr({transform:l,containerWidth:c,iconWidth:f}),O={tag:"rect",attributes:d(d({},de),{},{fill:"white"})},x=u.children?{children:u.children.map(Nn)}:{},h={tag:"g",attributes:d({},g.inner),children:[Nn(d({tag:u.tag,attributes:d(d({},u.attributes),g.path)},x))]},m={tag:"g",attributes:d({},g.outer),children:[h]},A="mask-".concat(s||_t()),k="clip-".concat(s||_t()),T={tag:"mask",attributes:d(d({},de),{},{id:A,maskUnits:"userSpaceOnUse",maskContentUnits:"userSpaceOnUse"}),children:[O,m]},w={tag:"defs",children:[{tag:"clipPath",attributes:{id:k},children:Ji(v)},T]};return a.push(w,{tag:"rect",attributes:d({fill:"currentColor","clip-path":"url(#".concat(k,")"),mask:"url(#".concat(A,")")},de)}),{children:a,attributes:r}}}},Zi={provides:function(e){var n=!1;rt.matchMedia&&(n=rt.matchMedia("(prefers-reduced-motion: reduce)").matches),e.missingIconAbstract=function(){var a=[],r={fill:"currentColor"},i={attributeType:"XML",repeatCount:"indefinite",dur:"2s"};a.push({tag:"path",attributes:d(d({},r),{},{d:"M156.5,447.7l-12.6,29.5c-18.7-9.5-35.9-21.2-51.5-34.9l22.7-22.7C127.6,430.5,141.5,440,156.5,447.7z M40.6,272H8.5 c1.4,21.2,5.4,41.7,11.7,61.1L50,321.2C45.1,305.5,41.8,289,40.6,272z M40.6,240c1.4-18.8,5.2-37,11.1-54.1l-29.5-12.6 C14.7,194.3,10,216.7,8.5,240H40.6z M64.3,156.5c7.8-14.9,17.2-28.8,28.1-41.5L69.7,92.3c-13.7,15.6-25.5,32.8-34.9,51.5 L64.3,156.5z M397,419.6c-13.9,12-29.4,22.3-46.1,30.4l11.9,29.8c20.7-9.9,39.8-22.6,56.9-37.6L397,419.6z M115,92.4 c13.9-12,29.4-22.3,46.1-30.4l-11.9-29.8c-20.7,9.9-39.8,22.6-56.8,37.6L115,92.4z M447.7,355.5c-7.8,14.9-17.2,28.8-28.1,41.5 l22.7,22.7c13.7-15.6,25.5-32.9,34.9-51.5L447.7,355.5z M471.4,272c-1.4,18.8-5.2,37-11.1,54.1l29.5,12.6 c7.5-21.1,12.2-43.5,13.6-66.8H471.4z M321.2,462c-15.7,5-32.2,8.2-49.2,9.4v32.1c21.2-1.4,41.7-5.4,61.1-11.7L321.2,462z M240,471.4c-18.8-1.4-37-5.2-54.1-11.1l-12.6,29.5c21.1,7.5,43.5,12.2,66.8,13.6V471.4z M462,190.8c5,15.7,8.2,32.2,9.4,49.2h32.1 c-1.4-21.2-5.4-41.7-11.7-61.1L462,190.8z M92.4,397c-12-13.9-22.3-29.4-30.4-46.1l-29.8,11.9c9.9,20.7,22.6,39.8,37.6,56.9 L92.4,397z M272,40.6c18.8,1.4,36.9,5.2,54.1,11.1l12.6-29.5C317.7,14.7,295.3,10,272,8.5V40.6z M190.8,50 c15.7-5,32.2-8.2,49.2-9.4V8.5c-21.2,1.4-41.7,5.4-61.1,11.7L190.8,50z M442.3,92.3L419.6,115c12,13.9,22.3,29.4,30.5,46.1 l29.8-11.9C470,128.5,457.3,109.4,442.3,92.3z M397,92.4l22.7-22.7c-15.6-13.7-32.8-25.5-51.5-34.9l-12.6,29.5 C370.4,72.1,384.4,81.5,397,92.4z"})});var o=d(d({},i),{},{attributeName:"opacity"}),s={tag:"circle",attributes:d(d({},r),{},{cx:"256",cy:"364",r:"28"}),children:[]};return n||s.children.push({tag:"animate",attributes:d(d({},i),{},{attributeName:"r",values:"28;14;28;28;14;28;"})},{tag:"animate",attributes:d(d({},o),{},{values:"1;0;1;1;0;1;"})}),a.push(s),a.push({tag:"path",attributes:d(d({},r),{},{opacity:"1",d:"M263.7,312h-16c-6.6,0-12-5.4-12-12c0-71,77.4-63.9,77.4-107.8c0-20-17.8-40.2-57.4-40.2c-29.1,0-44.3,9.6-59.2,28.7 c-3.9,5-11.1,6-16.2,2.4l-13.1-9.2c-5.6-3.9-6.9-11.8-2.6-17.2c21.2-27.2,46.4-44.7,91.2-44.7c52.3,0,97.4,29.8,97.4,80.2 c0,67.6-77.4,63.5-77.4,107.8C275.7,306.6,270.3,312,263.7,312z"}),children:n?[]:[{tag:"animate",attributes:d(d({},o),{},{values:"1;0;0;0;0;1;"})}]}),n||a.push({tag:"path",attributes:d(d({},r),{},{opacity:"0",d:"M232.5,134.5l7,168c0.3,6.4,5.6,11.5,12,11.5h9c6.4,0,11.7-5.1,12-11.5l7-168c0.3-6.8-5.2-12.5-12-12.5h-23 C237.7,122,232.2,127.7,232.5,134.5z"}),children:[{tag:"animate",attributes:d(d({},o),{},{values:"0;0;1;1;0;0;"})}]}),{tag:"g",attributes:{class:"missing"},children:a}}}},to={hooks:function(){return{parseNodeAttributes:function(n,a){var r=a.getAttribute("data-fa-symbol"),i=r===null?!1:r===""?!0:r;return n.symbol=i,n}}}},eo=[Zr,Fi,Wi,Yi,Ui,Xi,qi,Ki,Qi,Zi,to];vi(eo,{mixoutsTo:D});D.noAuto;D.config;D.library;D.dom;var Re=D.parse;D.findIconDefinition;D.toHtml;var no=D.icon;D.layer;D.text;D.counter;var Na={exports:{}},ao="SECRET_DO_NOT_PASS_THIS_OR_YOU_WILL_BE_FIRED",ro=ao,io=ro;function _a(){}function $a(){}$a.resetWarningCache=_a;var oo=function(){function t(a,r,i,o,s,l){if(l!==io){var f=new Error("Calling PropTypes validators directly is not supported by the `prop-types` package. Use PropTypes.checkPropTypes() to call them. Read more at http://fb.me/use-check-prop-types");throw f.name="Invariant Violation",f}}t.isRequired=t;function e(){return t}var n={array:t,bigint:t,bool:t,func:t,number:t,object:t,string:t,symbol:t,any:t,arrayOf:e,element:t,elementType:t,instanceOf:e,node:t,objectOf:e,oneOf:e,oneOfType:e,shape:e,exact:e,checkPropTypes:$a,resetWarningCache:_a};return n.PropTypes=n,n};Na.exports=oo();var y=Na.exports;function _n(t,e){var n=Object.keys(t);if(Object.getOwnPropertySymbols){var a=Object.getOwnPropertySymbols(t);e&&(a=a.filter(function(r){return Object.getOwnPropertyDescriptor(t,r).enumerable})),n.push.apply(n,a)}return n}function at(t){for(var e=1;e<arguments.length;e++){var n=arguments[e]!=null?arguments[e]:{};e%2?_n(Object(n),!0).forEach(function(a){gt(t,a,n[a])}):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(n)):_n(Object(n)).forEach(function(a){Object.defineProperty(t,a,Object.getOwnPropertyDescriptor(n,a))})}return t}function Gt(t){return Gt=typeof Symbol=="function"&&typeof Symbol.iterator=="symbol"?function(e){return typeof e}:function(e){return e&&typeof Symbol=="function"&&e.constructor===Symbol&&e!==Symbol.prototype?"symbol":typeof e},Gt(t)}function gt(t,e,n){return e in t?Object.defineProperty(t,e,{value:n,enumerable:!0,configurable:!0,writable:!0}):t[e]=n,t}function so(t,e){if(t==null)return{};var n={},a=Object.keys(t),r,i;for(i=0;i<a.length;i++)r=a[i],!(e.indexOf(r)>=0)&&(n[r]=t[r]);return n}function Ma(t,e){if(t==null)return{};var n=so(t,e),a,r;if(Object.getOwnPropertySymbols){var i=Object.getOwnPropertySymbols(t);for(r=0;r<i.length;r++)a=i[r],!(e.indexOf(a)>=0)&&(!Object.prototype.propertyIsEnumerable.call(t,a)||(n[a]=t[a]))}return n}function Ne(t){return lo(t)||fo(t)||uo(t)||co()}function lo(t){if(Array.isArray(t))return _e(t)}function fo(t){if(typeof Symbol!="undefined"&&t[Symbol.iterator]!=null||t["@@iterator"]!=null)return Array.from(t)}function uo(t,e){if(!!t){if(typeof t=="string")return _e(t,e);var n=Object.prototype.toString.call(t).slice(8,-1);if(n==="Object"&&t.constructor&&(n=t.constructor.name),n==="Map"||n==="Set")return Array.from(t);if(n==="Arguments"||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(n))return _e(t,e)}}function _e(t,e){(e==null||e>t.length)&&(e=t.length);for(var n=0,a=new Array(e);n<e;n++)a[n]=t[n];return a}function co(){throw new TypeError(`Invalid attempt to spread non-iterable instance.
In order to be iterable, non-array objects must have a [Symbol.iterator]() method.`)}function mo(t){var e,n=t.beat,a=t.fade,r=t.beatFade,i=t.bounce,o=t.shake,s=t.flash,l=t.spin,f=t.spinPulse,u=t.spinReverse,c=t.pulse,v=t.fixedWidth,g=t.inverse,O=t.border,x=t.listItem,h=t.flip,m=t.size,A=t.rotation,k=t.pull,T=(e={"fa-beat":n,"fa-fade":a,"fa-beat-fade":r,"fa-bounce":i,"fa-shake":o,"fa-flash":s,"fa-spin":l,"fa-spin-reverse":u,"fa-spin-pulse":f,"fa-pulse":c,"fa-fw":v,"fa-inverse":g,"fa-border":O,"fa-li":x,"fa-flip-horizontal":h==="horizontal"||h==="both","fa-flip-vertical":h==="vertical"||h==="both"},gt(e,"fa-".concat(m),typeof m!="undefined"&&m!==null),gt(e,"fa-rotate-".concat(A),typeof A!="undefined"&&A!==null&&A!==0),gt(e,"fa-pull-".concat(k),typeof k!="undefined"&&k!==null),gt(e,"fa-swap-opacity",t.swapOpacity),e);return Object.keys(T).map(function(w){return T[w]?w:null}).filter(function(w){return w})}function vo(t){return t=t-0,t===t}function La(t){return vo(t)?t:(t=t.replace(/[\-_\s]+(.)?/g,function(e,n){return n?n.toUpperCase():""}),t.substr(0,1).toLowerCase()+t.substr(1))}var po=["style"];function bo(t){return t.charAt(0).toUpperCase()+t.slice(1)}function ho(t){return t.split(";").map(function(e){return e.trim()}).filter(function(e){return e}).reduce(function(e,n){var a=n.indexOf(":"),r=La(n.slice(0,a)),i=n.slice(a+1).trim();return r.startsWith("webkit")?e[bo(r)]=i:e[r]=i,e},{})}function Da(t,e){var n=arguments.length>2&&arguments[2]!==void 0?arguments[2]:{};if(typeof e=="string")return e;var a=(e.children||[]).map(function(l){return Da(t,l)}),r=Object.keys(e.attributes||{}).reduce(function(l,f){var u=e.attributes[f];switch(f){case"class":l.attrs.className=u,delete e.attributes.class;break;case"style":l.attrs.style=ho(u);break;default:f.indexOf("aria-")===0||f.indexOf("data-")===0?l.attrs[f.toLowerCase()]=u:l.attrs[La(f)]=u}return l},{attrs:{}}),i=n.style,o=i===void 0?{}:i,s=Ma(n,po);return r.attrs.style=at(at({},r.attrs.style),o),t.apply(void 0,[e.tag,at(at({},r.attrs),s)].concat(Ne(a)))}var za=!1;try{za=!0}catch{}function go(){if(!za&&console&&typeof console.error=="function"){var t;(t=console).error.apply(t,arguments)}}function $n(t){if(t&&Gt(t)==="object"&&t.prefix&&t.iconName&&t.icon)return t;if(Re.icon)return Re.icon(t);if(t===null)return null;if(t&&Gt(t)==="object"&&t.prefix&&t.iconName)return t;if(Array.isArray(t)&&t.length===2)return{prefix:t[0],iconName:t[1]};if(typeof t=="string")return{prefix:"fas",iconName:t}}function me(t,e){return Array.isArray(e)&&e.length>0||!Array.isArray(e)&&e?gt({},t,e):{}}var yo=["forwardedRef"];function mt(t){var e=t.forwardedRef,n=Ma(t,yo),a=n.icon,r=n.mask,i=n.symbol,o=n.className,s=n.title,l=n.titleId,f=n.maskId,u=$n(a),c=me("classes",[].concat(Ne(mo(n)),Ne(o.split(" ")))),v=me("transform",typeof n.transform=="string"?Re.transform(n.transform):n.transform),g=me("mask",$n(r)),O=no(u,at(at(at(at({},c),v),g),{},{symbol:i,title:s,titleId:l,maskId:f}));if(!O)return go("Could not find icon",u),null;var x=O.abstract,h={ref:e};return Object.keys(n).forEach(function(m){mt.defaultProps.hasOwnProperty(m)||(h[m]=n[m])}),wo(x[0],h)}mt.displayName="FontAwesomeIcon";mt.propTypes={beat:y.bool,border:y.bool,bounce:y.bool,className:y.string,fade:y.bool,flash:y.bool,mask:y.oneOfType([y.object,y.array,y.string]),maskId:y.string,fixedWidth:y.bool,inverse:y.bool,flip:y.oneOf(["horizontal","vertical","both"]),icon:y.oneOfType([y.object,y.array,y.string]),listItem:y.bool,pull:y.oneOf(["right","left"]),pulse:y.bool,rotation:y.oneOf([0,90,180,270]),shake:y.bool,size:y.oneOf(["2xs","xs","sm","lg","xl","2xl","1x","2x","3x","4x","5x","6x","7x","8x","9x","10x"]),spin:y.bool,spinPulse:y.bool,spinReverse:y.bool,symbol:y.oneOfType([y.bool,y.string]),title:y.string,titleId:y.string,transform:y.oneOfType([y.string,y.object]),swapOpacity:y.bool};mt.defaultProps={border:!1,className:"",mask:null,maskId:null,fixedWidth:!1,inverse:!1,flip:null,icon:null,listItem:!1,pull:null,pulse:!1,rotation:null,size:null,spin:!1,beat:!1,fade:!1,beatFade:!1,bounce:!1,shake:!1,symbol:!1,title:"",titleId:null,transform:null,swapOpacity:!1};var wo=Da.bind(null,Yn.createElement);const xo=I("button",{cursor:"pointer",background:"none",border:"none",display:"flex",margin:0,padding:"$1",fontSize:"$3",fontWeight:"900",borderRadius:"4px","&:hover":{backgroundColor:"#D9D9D9"},"&:active":{backgroundColor:"$gray5"}}),ko=I("div",{borderRadius:"4px",filter:"drop-shadow(0px 2px 4px rgba(0, 0, 0, 0.16))",background:"$lightGray",cursor:"pointer",variants:{state:{focused:{outline:"2px solid $purpleStroke"},none:{}},clickable:{yes:{cursor:"pointer"},no:{cursor:"not-allowed"}}}}),Co=I("div",{$$borderRadius:"4px",display:"flex",alignItems:"center",gap:"$1",borderTopLeftRadius:"$$borderRadius",borderTopRightRadius:"$$borderRadius",fontSize:"$2",color:"$white",padding:"$1 $2",variants:{component:{app:{background:"$appCardColor"},job:{background:"$jobCardColor"},data:{background:"$dataCardColor"}}}}),Ao=I("div",{$$borderRadius:"4px",background:"$gray7CardBackground",padding:"$3 $2",borderBottomRightRadius:"$$borderRadius",borderBottomLeftRadius:"$$borderRadius"}),$e=I("div",{variants:{width:{mobile:{width:"100%"},tablet:{width:"45%"},desktop:{width:"320px"}}}}),ja=({type:t,metadata:e,title:n,isSelected:a,onClick:r})=>p($e,{width:{"@initial":"mobile","@bp1":"tablet","@bp2":"desktop"},children:P(ko,{state:a?"focused":"none",role:"button",onClick:r,clickable:r?"yes":"no",children:[p(Co,{component:t,children:e}),p(Ao,{children:p(vr,{margin:"none",children:n})})]})}),Mn=40,Oo=({app:t,onClick:e,isSelected:n})=>{var r;const a=i=>i.length>Mn?`${i.slice(0,Mn)}...`:i;return p(ja,{type:"app",isSelected:n,metadata:P(ut,{children:[p(mt,{icon:yr}),p(H,{margin:"none",color:"white",children:p(ye,{children:t.memory})}),P(H,{margin:"none",color:"white",children:[p(ye,{children:t.cpu})," CPU"]})]}),title:a((r=t.name)!=null?r:t.filename),onClick:()=>e(t)})},So=({schedule:t})=>p(ja,{type:"job",title:t.name,metadata:P(ut,{children:[p(mt,{icon:wr}),P(H,{color:"white",margin:"none",children:["Runs every ",p(ye,{children:t.seconds})," seconds"]})]})}),Eo=()=>{const{width:t,height:e}=C.exports.useContext(Un);return{width:t,height:e}},Ln=I(Me,{borderRadius:"5px",backgroundColor:"purple",padding:"$2",boxShadow:"0px 4px 6px rgba(0, 0, 0, 0.1)",width:"100%",variants:{color:{purple:{background:"$darkPurpleGradient",color:"$white"},black:{background:"$blackGradient",color:"$white"},gray:{background:"$lightGray",color:"$primaryDark"}},state:{focused:{outline:"1px solid $purpleStroke"},none:{}}},defaultVariants:{color:"purple"}}),Dn=I("div",{display:"flex",flexWrap:"wrap",gap:"$4"}),To=I("div",{display:"grid",gridTemplateColumns:"320px auto",gap:"$3"}),Io=I("div",{$$height:"90vh",height:"$$height",width:"100%","&>iframe":{border:0,height:"$$height",width:"100%"}}),zn=I("div",{}),Po=I("div",{width:"650px"}),Ro=t=>t.length>0?t[0]:null,No=({projectUrl:t,apps:e,schedules:n,headerContent:a,shouldAutoFocusFirstComponent:r})=>{const[i,o]=C.exports.useState(null),{width:s}=Eo();C.exports.useEffect(()=>{r&&o(Ro(e))},[r,e]);const l=u=>{window.location.replace(`${t}${u.route}`)},f=s>=Vn.BP2;return P(To,{children:[P("div",{children:[!f&&P(ut,{children:[a,p(st,{})]}),p(le,{children:"Apps"}),e.length>0?p(Dn,{children:e.map(u=>{const c=(i==null?void 0:i.uid)===u.uid;return p(Oo,{isSelected:c,onClick:()=>{f?o(c?null:u):l(u)},app:u},u.uid)})}):p($e,{width:{"@initial":"mobile","@bp1":"tablet","@bp2":"desktop"},children:p(Ln,{color:"gray",css:{textAlign:"center"},children:p(H,{weight:"big",margin:"none",children:"No apps"})})}),p(st,{}),p(le,{children:"Jobs"}),n.length>0?p(Dn,{children:n.map(u=>p(So,{schedule:u},u.uid))}):p($e,{width:{"@initial":"mobile","@bp1":"tablet","@bp2":"desktop"},children:p(Ln,{color:"gray",css:{textAlign:"center"},children:p(H,{weight:"big",margin:"none",children:"No jobs"})})})]}),f&&p(Io,{children:i?P(ut,{children:[P(Wn,{css:{justifyContent:"space-between",alignItems:"center"},children:[p(zn,{css:{display:"flex",alignItems:"center",gap:"$1"},children:p(le,{children:i.name})}),p(zn,{css:{display:"flex",gap:"$1",alignItems:"flex-start"},children:p(xo,{onClick:()=>o(null),children:p(mt,{icon:xr})})})]}),p("iframe",{src:`${t}${i.route}`,title:i.name})]}):p(Po,{children:a})})]})},jn=I(Me,{display:"flex",justifyContent:"center",alignItems:"center",gap:"$3"}),_o=I(Me,{display:"flex",paddingX:"$3",height:"60px",backgroundColor:"$primaryDark",flexDirection:"row",alignItems:"center",justifyContent:"space-between",transition:"0.2s ease-in",width:"100%"}),$o=({projectName:t})=>P(_o,{children:[P(jn,{children:[p("img",{src:"/logo.png",height:"30px",width:"30px",alt:"Databutton"}),t&&p(H,{color:"white",margin:"none",children:t})]}),P(jn,{children:[p(Yt,{href:"https://docs.databutton.com",target:"_blank",rel:"noreferrer",color:"white",weight:"semiBold",children:"Documentation"}),p(Yt,{href:"https://next.databutton.com",target:"_blank",rel:"noreferrer",children:p(Ua,{children:"databutton.com"})})]})]}),Fn="http://localhost:8000";function Mo(){const{data:t}=mr(`${Fn}/static/artifacts.json`,a=>fetch(a).then(r=>r.json()),{refreshInterval:500}),e=C.exports.useMemo(()=>t?t.streamlit_apps:[],[t]),n=(t==null?void 0:t.streamlit_apps.length)===0&&t.schedules.length===0;return P(ut,{children:[p($o,{}),p(gr,{children:n?p(hr,{localOrCloud:"local"}):p(No,{projectUrl:Fn,shouldAutoFocusFirstComponent:e.length===1,apps:e,schedules:t?t.schedules:[]})})]})}Va.createRoot(document.getElementById("root")).render(p(Yn.StrictMode,{children:p(Ha,{children:p(Mo,{})})}));
