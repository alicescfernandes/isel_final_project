(()=>{var l=Object.create;var h=Object.defineProperty;var c=Object.getOwnPropertyDescriptor;var d=Object.getOwnPropertyNames;var u=Object.getPrototypeOf,p=Object.prototype.hasOwnProperty;var v=(s=>typeof require<"u"?require:typeof Proxy<"u"?new Proxy(s,{get:(t,e)=>(typeof require<"u"?require:t)[e]}):s)(function(s){if(typeof require<"u")return require.apply(this,arguments);throw Error('Dynamic require of "'+s+'" is not supported')});var f=(s,t,e,i)=>{if(t&&typeof t=="object"||typeof t=="function")for(let r of d(t))!p.call(s,r)&&r!==e&&h(s,r,{get:()=>t[r],enumerable:!(i=c(t,r))||i.enumerable});return s};var g=(s,t,e)=>(e=s!=null?l(u(s)):{},f(t||!s||!s.__esModule?h(e,"default",{value:s,enumerable:!0}):e,s));var C="http://localhost:8000/api/",n=class extends HTMLElement{constructor(){super(),this.id=`chart_${Math.floor(Math.random()*1e6)}`,this.state={chartSlug:this.getAttribute("chart_slug"),quarterNumber:this.getAttribute("q"),isError:!1,isLoading:!0}}static get observedAttributes(){return["chart_slug"]}connectedCallback(){this.setupLazyLoad()}fetchData(){let t=new URLSearchParams;t.set("slug",this.state.chartSlug),t.set("q",this.state.quarterNumber),this.state.selectedOption&&t.set("opt",this.state.selectedOption),fetch(`${C}chart/?${t.toString()}`).then(e=>{if(!e.ok)throw new Error(`HTTP error! Status: ${response.status}`);return e.json()}).then(e=>{let{selected_option:i,...r}=e;this.setState({selectedOption:i||"",...r})}).catch(()=>{this.setState({isError:!0})}).finally(()=>{this.setState({isLoading:!1})})}setState(t){this.state={...this.state,...t},this.render()}renderQuarterNavigation(){let t=this.querySelector(`#${this.id} .chart-quarter-navigation`),{quarter:e}=this.state;t.innerHTML=`
        <button ${!e.prev&&"disabled"} aria-label="Previous Quarter" class="prev-quarter chart-quarter-text">\u2190</button>
        <button ${!e.next&&"disabled"} aria-label="Next Quarter" class="next-quarter chart-quarter-text">\u2192</button>`}renderSpinner(){this.innerHTML=`<div role="status" class="spinner-container">
                            <svg aria-hidden="true" class="spinner-svg" fill="none" viewBox="0 0 100 101 xmlns="http://www.w3.org/2000/svg">
                                <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                                <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                            </svg>
                            <span class="sr-only">Loading...</span>
                        </div>
                    `}renderError(){this.innerHTML=`
            <div class="alert-error" role="alert">
            <svg class="alert-error-svg" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
            </svg>
            <span class="sr-only">Info</span>
            <div>
                <span class="font-bold">Unable to render chart.</span> Try uploading a new one with the data.
            </div>
            </div>
        `}renderEmptyState(){return`
            <div class="alert-info" role="alert">
                <svg class="shrink-0 inline w-4 h-4 me-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/>
                </svg>
                <span class="sr-only">Info</span>
                <div>
                    The graph doesn't have data to show.
                </div>
            </div>
        `}render(){let t=!!(this.state.options&&this.state.options.length>0);if(this.state.isLoading)return this.renderSpinner();if(this.state.isError)return this.renderError();this.innerHTML=`<div id="${this.id}"> 
                <div class="chart-header">
                    <h5 class="chart-title"></h5>
                    <div class="chart-quarter-navigation">
                    </div>
                </div>
                
                ${t?`
                    <p> Filter By: 
                    <select class="chart-filter"></select>
                    </p>`:""}
                <div class="chart" style="width:100%;height:400px;"></div>
                </div>`,this.renderChart(),this.renderQuarterNavigation(),t&&(this.renderOptions(),this.setupEvents())}attributeChangedCallback(){!!this.state.option&&(this.renderOptions(),this.setupEvents()),this.renderChart()}renderOptions(){let t=this.querySelector(`#${this.id} .chart-filter`);if(!t)return;let{options:e,selectedOption:i}=this.state;t.innerHTML="";for(let r of e){let a=document.createElement("option");a.value=r,a.textContent=r,a.selected=r===i,t.appendChild(a)}}setupLazyLoad(){new IntersectionObserver((e,i)=>{for(let r of e)r.isIntersecting&&(this.loadChart(),i.unobserve(this))},{root:null,rootMargin:"100px",threshold:.1}).observe(this)}loadChart(){this.state.isLoading&&(this.fetchData(),this.render())}setupEvents(){let t=this.querySelector(`#${this.id} .chart-filter`);t&&t.addEventListener("change",r=>{let a=r.target.value;this.setState({selectedOption:a}),this.fetchData()});let e=this.querySelector(`#${this.id} .prev-quarter`);e&&e.addEventListener("click",r=>{this.setState({quarterNumber:this.state.quarter.prev}),this.fetchData()});let i=this.querySelector(`#${this.id} .next-quarter`);i&&i.addEventListener("click",r=>{this.setState({quarterNumber:this.state.quarter.next}),this.fetchData()})}async renderChart(){if(!this.isConnected||this.state.isLoading)return;let{title:t,chart_config:e}=this.state,{traces:i,layout:r}=e,a=this.querySelector(`#${this.id} .chart`),o=this.querySelector(`#${this.id} .chart-title`);if(o&&(o.textContent=`${t} - Q${this.state.quarter.current}`),i.length<=0){a.innerHTML=this.renderEmptyState();return}window.Plotly||await import("https://cdn.plot.ly/plotly-2.30.0.min.js"),a&&Plotly.newPlot(a,i,r,{responsive:!0})}};window.addEventListener("load",()=>{customElements.define("plotly-chart",n)});})();
//# sourceMappingURL=chart_webcomponent.js.map
