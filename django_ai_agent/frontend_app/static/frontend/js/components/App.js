import React, { useState, useEffect } from 'react';

// Language translations
const translations = {
    en: {
        "app-title": "AI Information Gathering Agent",
        "dashboard-tab": "Dashboard",
        "scans-tab": "Scans",
        "keywords-tab": "Keywords",
        "reports-tab": "Reports",
        "config-tab": "Configuration",
        "chat-tab": "AI Chat",
        "loading-title": "Loading...",
        "loading-message": "Please wait while we prepare your dashboard",
        "dashboard-title": "Dashboard",
        "total-scans": "Total Scans",
        "active-scans": "Active Scans",
        "generated-reports": "Generated Reports",
        "saved-configs": "Saved Configurations",
        "recent-activity": "Recent Activity",
        "scan-action": "Started scan on",
        "report-action": "Generated report for",
        "config-action": "Updated configuration settings",
        "scans-title": "Start New Scan",
        "target-label": "Target:",
        "target-placeholder": "Enter domain or IP address",
        "modules-label": "Modules:",
        "whois-module": "WHOIS",
        "domain-module": "Domain Information",
        "port-module": "Port Scanning",
        "sensitive-module": "Sensitive Information",
        "github-module": "GitHub Search",
        "start-scan-button": "Start Scan",
        "scan-history": "Scan History",
        "target-header": "Target",
        "date-header": "Date",
        "status-header": "Status",
        "actions-header": "Actions",
        "view-results": "View Results",
        "generate-report": "Generate Report",
        "completed-status": "Completed",
        "keywords-title": "Keyword Management",
        "add-keyword-title": "Add New Keyword",
        "name-label": "Name:",
        "name-placeholder": "Enter keyword or name",
        "description-label": "Description:",
        "description-placeholder": "Enter description",
        "add-keyword-button": "Add Keyword",
        "managed-keywords": "Managed Keywords",
        "name-header": "Name",
        "description-header": "Description",
        "status-header": "Status",
        "actions-header": "Actions",
        "active-status": "Active",
        "inactive-status": "Inactive",
        "deactivate-button": "Deactivate",
        "activate-button": "Activate",
        "reports-title": "Generated Reports",
        "generate-report-button": "Generate New Report",
        "export-reports-button": "Export All Reports",
        "title-header": "Title",
        "type-header": "Type",
        "format-header": "Format",
        "view-button": "View",
        "download-button": "Download",
        "config-title": "System Configuration",
        "platform-settings": "Platform Settings",
        "platform-header": "Platform",
        "url-header": "URL",
        "status-header": "Status",
        "actions-header": "Actions",
        "deactivate-button": "Deactivate",
        "activate-button": "Activate",
        "edit-button": "Edit",
        "add-platform-button": "Add New Platform",
        "ai-model-settings": "AI Model Settings",
        "model-header": "Model",
        "provider-header": "Provider",
        "status-header": "Status",
        "actions-header": "Actions",
        "deactivate-button": "Deactivate",
        "activate-button": "Activate",
        "edit-button": "Edit",
        "add-model-button": "Add New AI Model",
        "chat-title": "AI Assistant",
        "ai-greeting": "Hello! I'm your AI assistant. How can I help you today?",
        "chat-placeholder": "Type your message here...",
        "send-button": "Send",
        "please-enter-target": "Please enter a target",
        "starting-scan": "Starting scan on",
        "with-modules": "with modules:",
        "please-enter-keyword": "Please enter a keyword name",
        "ten-minutes-ago": "10 minutes ago",
        "twenty-five-minutes-ago": "25 minutes ago",
        "one-hour-ago": "1 hour ago"
    },
    zh: {
        "app-title": "AI信息收集代理",
        "dashboard-tab": "仪表板",
        "scans-tab": "扫描",
        "keywords-tab": "关键词",
        "reports-tab": "报告",
        "config-tab": "配置",
        "chat-tab": "AI聊天",
        "loading-title": "加载中...",
        "loading-message": "请稍候，我们正在准备您的仪表板",
        "dashboard-title": "仪表板",
        "total-scans": "总扫描数",
        "active-scans": "活动扫描",
        "generated-reports": "生成报告",
        "saved-configs": "保存配置",
        "recent-activity": "最近活动",
        "scan-action": "开始扫描",
        "report-action": "生成报告给",
        "config-action": "更新配置设置",
        "scans-title": "开始新扫描",
        "target-label": "目标:",
        "target-placeholder": "输入域名或IP地址",
        "modules-label": "模块:",
        "whois-module": "WHOIS",
        "domain-module": "域名信息",
        "port-module": "端口扫描",
        "sensitive-module": "敏感信息",
        "github-module": "GitHub搜索",
        "start-scan-button": "开始扫描",
        "scan-history": "扫描历史",
        "target-header": "目标",
        "date-header": "日期",
        "status-header": "状态",
        "actions-header": "操作",
        "view-results": "查看结果",
        "generate-report": "生成报告",
        "completed-status": "已完成",
        "keywords-title": "关键词管理",
        "add-keyword-title": "添加新关键词",
        "name-label": "名称:",
        "name-placeholder": "输入关键词或名称",
        "description-label": "描述:",
        "description-placeholder": "输入描述",
        "add-keyword-button": "添加关键词",
        "managed-keywords": "管理的关键词",
        "name-header": "名称",
        "description-header": "描述",
        "status-header": "状态",
        "actions-header": "操作",
        "active-status": "激活",
        "inactive-status": "未激活",
        "deactivate-button": "停用",
        "activate-button": "激活",
        "reports-title": "生成的报告",
        "generate-report-button": "生成新报告",
        "export-reports-button": "导出所有报告",
        "title-header": "标题",
        "type-header": "类型",
        "format-header": "格式",
        "view-button": "查看",
        "download-button": "下载",
        "config-title": "系统配置",
        "platform-settings": "平台设置",
        "platform-header": "平台",
        "url-header": "网址",
        "status-header": "状态",
        "actions-header": "操作",
        "deactivate-button": "停用",
        "activate-button": "激活",
        "edit-button": "编辑",
        "add-platform-button": "添加新平台",
        "ai-model-settings": "AI模型设置",
        "model-header": "模型",
        "provider-header": "提供商",
        "status-header": "状态",
        "actions-header": "操作",
        "deactivate-button": "停用",
        "activate-button": "激活",
        "edit-button": "编辑",
        "add-model-button": "添加新AI模型",
        "chat-title": "AI助手",
        "ai-greeting": "你好！我是你的AI助手。今天我能帮你什么？",
        "chat-placeholder": "在这里输入你的消息...",
        "send-button": "发送",
        "please-enter-target": "请输入目标",
        "starting-scan": "开始扫描",
        "with-modules": "使用模块:",
        "please-enter-keyword": "请输入关键词名称",
        "ten-minutes-ago": "10分钟前",
        "twenty-five-minutes-ago": "25分钟前",
        "one-hour-ago": "1小时前"
    }
};

const App = () => {
        const [activeTab, setActiveTab] = useState('dashboard');
        const [isLoading, setIsLoading] = useState(false);
        const [message, setMessage] = useState('');
        const [language, setLanguage] = useState('en');

        // Get language from localStorage on initial load
        useEffect(() => {
            const savedLanguage = localStorage.getItem('preferredLanguage') || 'en';
            setLanguage(savedLanguage);
        }, []);

        // Navigation function
        const navigateTo = (tab) => {
            setActiveTab(tab);
            // In a real app, you would update the URL here
        };

        // Simulate loading data
        useEffect(() => {
            setIsLoading(true);
            // Simulate API call
            setTimeout(() => {
                setIsLoading(false);
            }, 1000);
        }, []);

        // Get translated text
        const t = (key) => {
            return translations[language][key] || key;
        };

        return ( <
                div className = "app" > { /* Header */ } <
                header className = "app-header" >
                <
                h1 > { t('app-title') } < /h1> <
                nav className = "main-nav" >
                <
                ul >
                <
                li >
                <
                button className = { activeTab === 'dashboard' ? 'active' : '' }
                onClick = {
                    () => navigateTo('dashboard') } >
                { t('dashboard-tab') } <
                /button> <
                /li> <
                li >
                <
                button className = { activeTab === 'scans' ? 'active' : '' }
                onClick = {
                    () => navigateTo('scans') } >
                { t('scans-tab') } <
                /button> <
                /li> <
                li >
                <
                button className = { activeTab === 'keywords' ? 'active' : '' }
                onClick = {
                    () => navigateTo('keywords') } >
                { t('keywords-tab') } <
                /button> <
                /li> <
                li >
                <
                button className = { activeTab === 'reports' ? 'active' : '' }
                onClick = {
                    () => navigateTo('reports') } >
                { t('reports-tab') } <
                /button> <
                /li> <
                li >
                <
                button className = { activeTab === 'config' ? 'active' : '' }
                onClick = {
                    () => navigateTo('config') } >
                { t('config-tab') } <
                /button> <
                /li> <
                li >
                <
                button className = { activeTab === 'chat' ? 'active' : '' }
                onClick = {
                    () => navigateTo('chat') } >
                { t('chat-tab') } <
                /button> <
                /li> <
                /ul> <
                /nav> <
                /header>

                { /* Main Content */ } <
                main className = "app-main" > {
                    isLoading ? ( <
                        div className = "loading" >
                        <
                        h2 > { t('loading-title') } < /h2> <
                        p > { t('loading-message') } < /p> <
                        /div>
                    ) : ( <
                            > {
                                activeTab === 'dashboard' && < Dashboard t = { t }
                                language = { language }
                                />} {
                                    activeTab === 'scans' && < Scans t = { t }
                                    language = { language }
                                    />} {
                                        activeTab === 'keywords' && < Keywords t = { t }
                                        language = { language }
                                        />} {
                                            activeTab === 'reports' && < Reports t = { t }
                                            language = { language }
                                            />} {
                                                activeTab === 'config' && < Configuration t = { t }
                                                language = { language }
                                                />} {
                                                    activeTab === 'chat' && < AIChat t = { t }
                                                    language = { language }
                                                    />} <
                                                    />
                                                )
                                            } <
                                            /main>

                                            { /* Footer */ } <
                                            footer className = "app-footer" >
                                                <
                                                p > & copy;
                                            2026 { t('app-title') }.All rights reserved. < /p> <
                                                /footer>

                                            { /* Notification System */ } {
                                                message && ( <
                                                    div className = "notification" >
                                                    <
                                                    p > { message } < /p> <
                                                    button onClick = {
                                                        () => setMessage('') } > × < /button> <
                                                    /div>
                                                )
                                            } <
                                            /div>
                                        );
                                    };

                                    // Dashboard Component
                                    const Dashboard = ({ t, language }) => {
                                        return ( <
                                            div className = "dashboard" >
                                            <
                                            h2 > { t('dashboard-title') } < /h2> <
                                            div className = "stats-grid" >
                                            <
                                            div className = "stat-card" >
                                            <
                                            h3 > { t('total-scans') } < /h3> <
                                            p > 12 < /p> <
                                            /div> <
                                            div className = "stat-card" >
                                            <
                                            h3 > { t('active-scans') } < /h3> <
                                            p > 3 < /p> <
                                            /div> <
                                            div className = "stat-card" >
                                            <
                                            h3 > { t('generated-reports') } < /h3> <
                                            p > 8 < /p> <
                                            /div> <
                                            div className = "stat-card" >
                                            <
                                            h3 > { t('saved-configs') } < /h3> <
                                            p > 5 < /p> <
                                            /div> <
                                            /div>

                                            <
                                            div className = "recent-activity" >
                                            <
                                            h3 > { t('recent-activity') } < /h3> <
                                            ul >
                                            <
                                            li > { t('scan-action') }
                                            example.com - { t('ten-minutes-ago') } < /li> <
                                            li > { t('report-action') }
                                            test.org - { t('twenty-five-minutes-ago') } < /li> <
                                            li > { t('config-action') } - { t('one-hour-ago') } < /li> <
                                            /ul> <
                                            /div> <
                                            /div>
                                        );
                                    };

                                    // Scans Component
                                    const Scans = ({ t, language }) => {
                                        const [target, setTarget] = useState('');
                                        const [modules, setModules] = useState({
                                            whois: true,
                                            domain: true,
                                            port: true,
                                            sensitive: true,
                                            github: true
                                        });

                                        const handleModuleChange = (module) => {
                                            setModules({
                                                ...modules,
                                                [module]: !modules[module]
                                            });
                                        };

                                        const startScan = () => {
                                            if (!target) {
                                                alert(t('please-enter-target'));
                                                return;
                                            }

                                            // In a real app, this would call the API
                                            alert(`${t('starting-scan')} ${target} ${t('with-modules')} ${Object.keys(modules).filter(m => modules[m]).join(', ')}`);
                                        };

                                        return ( <
                                            div className = "scans" >
                                            <
                                            h2 > { t('scans-title') } < /h2> <
                                            div className = "scan-form" >
                                            <
                                            div className = "form-group" >
                                            <
                                            label htmlFor = "target" > { t('target-label') } < /label> <
                                            input type = "text"
                                            id = "target"
                                            value = { target }
                                            onChange = {
                                                (e) => setTarget(e.target.value) }
                                            placeholder = { t('target-placeholder') }
                                            /> <
                                            /div>

                                            <
                                            div className = "form-group" >
                                            <
                                            label > { t('modules-label') } < /label> <
                                            div className = "checkbox-group" >
                                            <
                                            label >
                                            <
                                            input type = "checkbox"
                                            checked = { modules.whois }
                                            onChange = {
                                                () => handleModuleChange('whois') }
                                            /> { t('whois-module') } <
                                            /label> <
                                            label >
                                            <
                                            input type = "checkbox"
                                            checked = { modules.domain }
                                            onChange = {
                                                () => handleModuleChange('domain') }
                                            /> { t('domain-module') } <
                                            /label> <
                                            label >
                                            <
                                            input type = "checkbox"
                                            checked = { modules.port }
                                            onChange = {
                                                () => handleModuleChange('port') }
                                            /> { t('port-module') } <
                                            /label> <
                                            label >
                                            <
                                            input type = "checkbox"
                                            checked = { modules.sensitive }
                                            onChange = {
                                                () => handleModuleChange('sensitive') }
                                            /> { t('sensitive-module') } <
                                            /label> <
                                            label >
                                            <
                                            input type = "checkbox"
                                            checked = { modules.github }
                                            onChange = {
                                                () => handleModuleChange('github') }
                                            /> { t('github-module') } <
                                            /label> <
                                            /div> <
                                            /div>

                                            <
                                            button className = "btn-primary"
                                            onClick = { startScan } > { t('start-scan-button') } <
                                            /button> <
                                            /div>

                                            <
                                            div className = "scan-history" >
                                            <
                                            h3 > { t('scan-history') } < /h3> <
                                            table >
                                            <
                                            thead >
                                            <
                                            tr >
                                            <
                                            th > { t('target-header') } < /th> <
                                            th > { t('date-header') } < /th> <
                                            th > { t('status-header') } < /th> <
                                            th > { t('actions-header') } < /th> <
                                            /tr> <
                                            /thead> <
                                            tbody >
                                            <
                                            tr >
                                            <
                                            td > example.com < /td> <
                                            td > 2026 - 02 - 23 01: 30: 00 < /td> <
                                            td > { t('completed-status') } < /td> <
                                            td >
                                            <
                                            button className = "btn-small" > { t('view-results') } < /button> <
                                            button className = "btn-small" > { t('generate-report') } < /button> <
                                            /td> <
                                            /tr> <
                                            tr >
                                            <
                                            td > test.org < /td> <
                                            td > 2026 - 02 - 22 15: 45: 00 < /td> <
                                            td > { t('completed-status') } < /td> <
                                            td >
                                            <
                                            button className = "btn-small" > { t('view-results') } < /button> <
                                            button className = "btn-small" > { t('generate-report') } < /button> <
                                            /td> <
                                            /tr> <
                                            /tbody> <
                                            /table> <
                                            /div> <
                                            /div>
                                        );
                                    };

                                    // Keywords Component
                                    const Keywords = ({ t, language }) => {
                                        const [keywords, setKeywords] = useState([
                                            { id: 1, name: 'John Doe', description: 'CEO of Example Corp', active: true },
                                            { id: 2, name: 'Jane Smith', description: 'Developer at Tech Solutions', active: true },
                                            { id: 3, name: 'Acme Inc', description: 'Technology company', active: false }
                                        ]);
                                        const [newKeyword, setNewKeyword] = useState({ name: '', description: '' });

                                        const addKeyword = () => {
                                            if (!newKeyword.name) {
                                                alert(t('please-enter-keyword'));
                                                return;
                                            }

                                            const keyword = {
                                                id: keywords.length + 1,
                                                name: newKeyword.name,
                                                description: newKeyword.description,
                                                active: true
                                            };

                                            setKeywords([...keywords, keyword]);
                                            setNewKeyword({ name: '', description: '' });
                                        };

                                        const toggleKeyword = (id) => {
                                            setKeywords(keywords.map(k =>
                                                k.id === id ? {...k, active: !k.active } : k
                                            ));
                                        };

                                        return ( <
                                            div className = "keywords" >
                                            <
                                            h2 > { t('keywords-title') } < /h2>

                                            <
                                            div className = "add-keyword" >
                                            <
                                            h3 > { t('add-keyword-title') } < /h3> <
                                            div className = "form-group" >
                                            <
                                            label htmlFor = "keyword-name" > { t('name-label') } < /label> <
                                            input type = "text"
                                            id = "keyword-name"
                                            value = { newKeyword.name }
                                            onChange = {
                                                (e) => setNewKeyword({...newKeyword, name: e.target.value }) }
                                            placeholder = { t('name-placeholder') }
                                            /> <
                                            /div> <
                                            div className = "form-group" >
                                            <
                                            label htmlFor = "keyword-description" > { t('description-label') } < /label> <
                                            textarea id = "keyword-description"
                                            value = { newKeyword.description }
                                            onChange = {
                                                (e) => setNewKeyword({...newKeyword, description: e.target.value }) }
                                            placeholder = { t('description-placeholder') }
                                            /> <
                                            /div> <
                                            button className = "btn-primary"
                                            onClick = { addKeyword } > { t('add-keyword-button') } <
                                            /button> <
                                            /div>

                                            <
                                            div className = "keyword-list" >
                                            <
                                            h3 > { t('managed-keywords') } < /h3> <
                                            table >
                                            <
                                            thead >
                                            <
                                            tr >
                                            <
                                            th > { t('name-header') } < /th> <
                                            th > { t('description-header') } < /th> <
                                            th > { t('status-header') } < /th> <
                                            th > { t('actions-header') } < /th> <
                                            /tr> <
                                            /thead> <
                                            tbody > {
                                                keywords.map(keyword => ( <
                                                    tr key = { keyword.id } >
                                                    <
                                                    td > { keyword.name } < /td> <
                                                    td > { keyword.description } < /td> <
                                                    td > { keyword.active ? t('active-status') : t('inactive-status') } < /td> <
                                                    td >
                                                    <
                                                    button className = "btn-small"
                                                    onClick = {
                                                        () => toggleKeyword(keyword.id) } >
                                                    { keyword.active ? t('deactivate-button') : t('activate-button') } <
                                                    /button> <
                                                    /td> <
                                                    /tr>
                                                ))
                                            } <
                                            /tbody> <
                                            /table> <
                                            /div> <
                                            /div>
                                        );
                                    };

                                    // Reports Component
                                    const Reports = ({ t, language }) => {
                                        const [reports, setReports] = useState([
                                            { id: 1, title: 'Scan Report - example.com', date: '2026-02-23', type: 'Scan', format: 'DOCX' },
                                            { id: 2, title: 'Keyword Analysis - John Doe', date: '2026-02-22', type: 'Keyword', format: 'PDF' },
                                            { id: 3, title: 'Combined Report', date: '2026-02-21', type: 'Combined', format: 'DOCX' }
                                        ]);

                                        return ( <
                                            div className = "reports" >
                                            <
                                            h2 > { t('reports-title') } < /h2>

                                            <
                                            div className = "report-actions" >
                                            <
                                            button className = "btn-primary" > { t('generate-report-button') } < /button> <
                                            button className = "btn-secondary" > { t('export-reports-button') } < /button> <
                                            /div>

                                            <
                                            div className = "report-list" >
                                            <
                                            table >
                                            <
                                            thead >
                                            <
                                            tr >
                                            <
                                            th > { t('title-header') } < /th> <
                                            th > { t('date-header') } < /th> <
                                            th > { t('type-header') } < /th> <
                                            th > { t('format-header') } < /th> <
                                            th > { t('actions-header') } < /th> <
                                            /tr> <
                                            /thead> <
                                            tbody > {
                                                reports.map(report => ( <
                                                    tr key = { report.id } >
                                                    <
                                                    td > { report.title } < /td> <
                                                    td > { report.date } < /td> <
                                                    td > { report.type } < /td> <
                                                    td > { report.format } < /td> <
                                                    td >
                                                    <
                                                    button className = "btn-small" > { t('view-button') } < /button> <
                                                    button className = "btn-small" > { t('download-button') } < /button> <
                                                    /td> <
                                                    /tr>
                                                ))
                                            } <
                                            /tbody> <
                                            /table> <
                                            /div> <
                                            /div>
                                        );
                                    };

                                    // Configuration Component
                                    const Configuration = ({ t, language }) => {
                                        const [platforms, setPlatforms] = useState([
                                            { id: 1, name: 'Xiaohongshu', url: 'https://xiaohongshu.com', active: true },
                                            { id: 2, name: 'Douyin', url: 'https://douyin.com', active: true },
                                            { id: 3, name: 'GitHub', url: 'https://github.com', active: true }
                                        ]);

                                        const [aiModels, setAiModels] = useState([
                                            { id: 1, name: 'GPT-4', provider: 'OpenAI', active: true },
                                            { id: 2, name: 'Claude 3', provider: 'Anthropic', active: true }
                                        ]);

                                        return ( <
                                            div className = "configuration" >
                                            <
                                            h2 > { t('config-title') } < /h2>

                                            <
                                            div className = "config-section" >
                                            <
                                            h3 > { t('platform-settings') } < /h3> <
                                            table >
                                            <
                                            thead >
                                            <
                                            tr >
                                            <
                                            th > { t('platform-header') } < /th> <
                                            th > { t('url-header') } < /th> <
                                            th > { t('status-header') } < /th> <
                                            th > { t('actions-header') } < /th> <
                                            /tr> <
                                            /thead> <
                                            tbody > {
                                                platforms.map(platform => ( <
                                                    tr key = { platform.id } >
                                                    <
                                                    td > { platform.name } < /td> <
                                                    td > { platform.url } < /td> <
                                                    td > { platform.active ? t('active-status') : t('inactive-status') } < /td> <
                                                    td >
                                                    <
                                                    button className = "btn-small" > { platform.active ? t('deactivate-button') : t('activate-button') } <
                                                    /button> <
                                                    button className = "btn-small" > { t('edit-button') } < /button> <
                                                    /td> <
                                                    /tr>
                                                ))
                                            } <
                                            /tbody> <
                                            /table>

                                            <
                                            button className = "btn-primary" > { t('add-platform-button') } < /button> <
                                            /div>

                                            <
                                            div className = "config-section" >
                                            <
                                            h3 > { t('ai-model-settings') } < /h3> <
                                            table >
                                            <
                                            thead >
                                            <
                                            tr >
                                            <
                                            th > { t('model-header') } < /th> <
                                            th > { t('provider-header') } < /th> <
                                            th > { t('status-header') } < /th> <
                                            th > { t('actions-header') } < /th> <
                                            /tr> <
                                            /thead> <
                                            tbody > {
                                                aiModels.map(model => ( <
                                                    tr key = { model.id } >
                                                    <
                                                    td > { model.name } < /td> <
                                                    td > { model.provider } < /td> <
                                                    td > { model.active ? t('active-status') : t('inactive-status') } < /td> <
                                                    td >
                                                    <
                                                    button className = "btn-small" > { model.active ? t('deactivate-button') : t('activate-button') } <
                                                    /button> <
                                                    button className = "btn-small" > { t('edit-button') } < /button> <
                                                    /td> <
                                                    /tr>
                                                ))
                                            } <
                                            /tbody> <
                                            /table>

                                            <
                                            button className = "btn-primary" > { t('add-model-button') } < /button> <
                                            /div> <
                                            /div>
                                        );
                                    };

                                    // AI Chat Component
                                    const AIChat = ({ t, language }) => {
                                        const [messages, setMessages] = useState([
                                            { id: 1, sender: 'ai', text: t('ai-greeting') }
                                        ]);
                                        const [input, setInput] = useState('');

                                        const sendMessage = () => {
                                            if (!input.trim()) return;

                                            // Add user message
                                            const userMessage = {
                                                id: messages.length + 1,
                                                sender: 'user',
                                                text: input
                                            };

                                            setMessages([...messages, userMessage]);

                                            // Simulate AI response
                                            setTimeout(() => {
                                                const aiResponse = {
                                                    id: messages.length + 2,
                                                    sender: 'ai',
                                                    text: `I understand you're asking about "${input}". This is a simulated response. In a real implementation, I would process your request and provide relevant information or execute commands.`
                                                };
                                                setMessages(prev => [...prev, aiResponse]);
                                            }, 1000);

                                            setInput('');
                                        };

                                        const handleKeyPress = (e) => {
                                            if (e.key === 'Enter') {
                                                sendMessage();
                                            }
                                        };

                                        return ( <
                                            div className = "ai-chat" >
                                            <
                                            h2 > { t('chat-title') } < /h2>

                                            <
                                            div className = "chat-container" >
                                            <
                                            div className = "chat-messages" > {
                                                messages.map(message => ( <
                                                    div key = { message.id }
                                                    className = { `message ${message.sender}` } >
                                                    <
                                                    div className = "message-content" > { message.text } < /div> <
                                                    /div>
                                                ))
                                            } <
                                            /div>

                                            <
                                            div className = "chat-input" >
                                            <
                                            input type = "text"
                                            value = { input }
                                            onChange = {
                                                (e) => setInput(e.target.value) }
                                            onKeyPress = { handleKeyPress }
                                            placeholder = { t('chat-placeholder') }
                                            /> <
                                            button className = "btn-primary"
                                            onClick = { sendMessage } > { t('send-button') } <
                                            /button> <
                                            /div> <
                                            /div> <
                                            /div>
                                        );
                                    };

                                    export default App;