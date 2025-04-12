(()=>{var h="http://localhost:8000/api/",i=class extends HTMLElement{constructor(){super(),this.id=`chart_${Math.floor(Math.random()*1e6)}`,this.initState()}initState(){this.state={chartSlug:this.getAttribute("chart_slug"),quarterNumber:this.getAttribute("q"),isError:!1,isLoading:!0}}static get observedAttributes(){return["chart_slug"]}connectedCallback(){this.setupLazyLoad()}async fetchData(){let t=new URLSearchParams({slug:this.state.chartSlug,q:this.state.quarterNumber,...this.state.selectedOption&&{opt:this.state.selectedOption}});try{let e=await fetch(`${h}chart/?${t.toString()}`);if(!e.ok)throw new Error(`HTTP error! Status: ${e.status}`);let s=await e.json(),{selected_option:r,...a}=s;this.setState({selectedOption:r||"",...a})}catch{this.setState({isError:!0})}finally{this.setState({isLoading:!1})}}setState(t){this.state={...this.state,...t},this.render()}render(){if(this.state.isLoading)return this.renderSpinner();if(this.state.isError)return this.renderError();let t=Array.isArray(this.state.options)&&this.state.options.length>0;this.innerHTML=`
            <div id="${this.id}">
                <div class="chart-header">
                    <h5 class="chart-title"></h5>
                    <div class="chart-quarter-navigation"></div>
                </div>
                ${t?'<p>Filter By: <select class="chart-filter"></select></p>':""}
                <div class="chart" style="width:100%;height:400px;"></div>
            </div>`,this.renderChart(),this.renderQuarterNavigation(),t&&(this.renderOptions(),this.setupEvents())}renderQuarterNavigation(){let t=this.querySelector(`#${this.id} .chart-quarter-navigation`),{quarter:e}=this.state;console.log("quarter",e,!e?.prev),t.innerHTML=`
            <button ${e?.prev?"":"disabled"} class="prev-quarter chart-quarter-nav-btn">\u2190</button>
            <button ${e?.next?"":"disabled"} class="next-quarter chart-quarter-nav-btn">\u2192</button>`}renderSpinner(){this.innerHTML=`<div class="spinner-container" role="status">
                                <svg aria-hidden="true" class="spinner-svg" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                                    <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="currentColor"/>
                                    <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentFill"/>
                                </svg>
                                <span class="sr-only">Loading...</span>`}renderError(){this.innerHTML=`
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
        `}renderOptions(){let t=this.querySelector(`#${this.id} .chart-filter`);if(!t)return;let{options:e,selectedOption:s}=this.state;t.innerHTML=e.map(r=>`<option value="${r}" ${r===s?"selected":""}>${r}</option>`).join("")}setupEvents(){this.querySelector(`#${this.id} .chart-filter`)?.addEventListener("change",t=>{this.setState({selectedOption:t.target.value}),this.fetchData()}),this.querySelector(`#${this.id} .prev-quarter`)?.addEventListener("click",()=>this.handleQuarterChange("prev")),this.querySelector(`#${this.id} .next-quarter`)?.addEventListener("click",()=>this.handleQuarterChange("next"))}handleQuarterChange(t){let e=this.state.quarter?.[t];e&&(this.setState({quarterNumber:e}),this.fetchData())}async renderChart(){if(!this.isConnected||this.state.isLoading)return;let{title:t,chart_config:e,quarter:s}=this.state,{traces:r,layout:a}=e,n=this.querySelector(`#${this.id} .chart`);if(this.querySelector(`#${this.id} .chart-title`).textContent=`${t} - Q${s.current}`,!r.length){n.innerHTML=this.renderEmptyState();return}Plotly.newPlot(n,r,a,{responsive:!0})}setupLazyLoad(){new IntersectionObserver((e,s)=>{for(let r of e)r.isIntersecting&&(this.loadChart(),s.unobserve(this))},{root:null,rootMargin:"100px",threshold:.1}).observe(this)}loadChart(){this.state.isLoading&&(this.fetchData(),this.render())}};window.addEventListener("load",()=>{customElements.define("plotly-chart",i)});})();
//# sourceMappingURL=chart_webcomponent.js.map
