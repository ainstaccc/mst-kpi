import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Button } from '@/components/ui/button.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Search, Filter, Download } from 'lucide-react'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('summary')
  const [filteredData, setFilteredData] = useState({
    summary: [],
    efficiency: [],
    manager_detail: [],
    staff_detail: []
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/data.json')
        const data = await response.json()
        
        // Filter out invalid records and clean data
        const cleanSummary = data.summary.filter(item => 
          item.部門編號 && 
          String(item.部門編號).toLowerCase() !== 'nan' && 
          item.人員姓名 &&
          String(item.人員姓名).toLowerCase() !== 'nan'
        ).map(item => ({
          ...item,
          員編: item.員編 ? String(Math.floor(item.員編)) : '',
          考核總分: item.考核總分 || '',
          管理項分數: item.管理項分數 || '',
          需訪談: item.需訪談 || ''
        }))

        const cleanEfficiency = data.efficiency.filter(item => 
          item.部門編號 && 
          String(item.部門編號).toLowerCase() !== 'nan' && 
          item.中文姓名 &&
          String(item.中文姓名).toLowerCase() !== 'nan'
        ).map(item => ({
          ...item,
          員工工號: item.員工工號 ? String(Math.floor(item.員工工號)) : '',
          個績目標: item.個績目標 || '',
          個績貢獻: item.個績貢獻 || '',
          '個績達成%': item['個績達成%'] || '',
          '品牌客單價': item['品牌\n客單價'] || '',
          '個人客單價': item['個人\n客單價'] || '',
          '客單相對績效': item['客單\n相對績效'] || '',
          '品牌結帳會員率': item['品牌\n結帳會員率'] || '',
          '個人結帳會員率': item['個人\n結帳會員率'] || '',
          '會員相對績效': item['會員\n相對績效'] || ''
        }))

        const cleanManagerDetail = data.manager_detail.filter(item => 
          item.部門編號 && 
          String(item.部門編號).toLowerCase() !== 'nan' && 
          item.人員姓名 &&
          String(item.人員姓名).toLowerCase() !== 'nan'
        ).map(item => ({
          ...item,
          員編: item.員編 ? String(Math.floor(item.員編)) : '',
          總分: item.總分 || '',
          '(1)營收達成': item['(1)營收達成'] || '',
          '(2)YOY加分項': item['(2)YOY加分項'] || '',
          業績項目分數: item.業績項目分數 || '',
          出勤異常: item.出勤異常 || '',
          管理分數_人資: item.管理分數_人資 || '',
          罰款: item.罰款 || '',
          帳差: item.帳差 || '',
          管理分數_財務: item.管理分數_財務 || '',
          驗收: item.驗收 || '',
          驗退: item.驗退 || '',
          管理分數_管理: item.管理分數_管理 || '',
          管理分數_服務: item.管理分數_服務 || '',
          'B+C總計30': item['B+C總計30'] || ''
        }))

        const cleanStaffDetail = data.staff_detail.filter(item => 
          item.部門編號 && 
          String(item.部門編號).toLowerCase() !== 'nan' && 
          item.人員姓名 &&
          String(item.人員姓名).toLowerCase() !== 'nan'
        ).map(item => ({
          ...item,
          員編: item.員編 ? String(Math.floor(item.員編)) : '',
          總分: item.總分 || '',
          店鋪業績分數: item.店鋪業績分數 || '',
          個績分數: item.個績分數 || '',
          '(4)個人客單': item['(4)個人客單'] || '',
          業績項目總分: item.業績項目總分 || '',
          個人出勤: item.個人出勤 || '',
          請假曠職: item.請假曠職 || '',
          管理分數B1: item.管理分數B1 || '',
          管理分數B2: item.管理分數B2 || '',
          管理分數C: item.管理分數C || '',
          'B+C總計30': item['B+C總計30'] || ''
        }))

        setFilteredData({
          summary: cleanSummary,
          efficiency: cleanEfficiency,
          manager_detail: cleanManagerDetail,
          staff_detail: cleanStaffDetail
        })
        setLoading(false)
      } catch (error) {
        console.error('Error loading data:', error)
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const renderTable = (data, title, count, highlightColumns = []) => {
    if (!data || data.length === 0) {
      return (
        <Card className="mb-6">
          <CardHeader className="bg-primary text-primary-foreground">
            <CardTitle className="text-lg font-bold">{title}</CardTitle>
          </CardHeader>
          <CardContent className="p-4">
            <div className="text-center text-muted-foreground">
              暫無資料
            </div>
            <div className="px-4 py-2 text-sm text-muted-foreground bg-muted/30 mt-4">
              [本次查詢共 0 筆]
            </div>
          </CardContent>
        </Card>
      )
    }

    return (
      <Card className="mb-6">
        <CardHeader className="bg-primary text-primary-foreground">
          <CardTitle className="text-lg font-bold">{title}</CardTitle>
        </CardHeader>
        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead className="bg-muted">
                <tr>
                  {Object.keys(data[0] || {}).map((key) => (
                    <th key={key} className="px-3 py-2 text-left font-medium border-r border-border last:border-r-0 whitespace-nowrap">
                      {key}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {data.slice(0, 50).map((row, index) => (
                  <tr key={index} className="border-b border-border hover:bg-muted/50">
                    {Object.entries(row).map(([key, value], cellIndex) => (
                      <td key={cellIndex} className={`px-3 py-2 border-r border-border last:border-r-0 whitespace-nowrap ${
                        highlightColumns.some(col => key.includes(col)) ? 'bg-accent/20 font-semibold' : ''
                      }`}>
                        {value === null || value === undefined || String(value).toLowerCase() === 'nan' ? '' : String(value)}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <div className="px-4 py-2 text-sm text-muted-foreground bg-muted/30">
            [本次查詢共 {count} 筆] {data.length > 50 && '(顯示前50筆)'}
          </div>
        </CardContent>
      </Card>
    )
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-background flex items-center justify-center">
        <div className="text-center">
          <div className="text-lg font-semibold">載入中...</div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="bg-secondary text-secondary-foreground shadow-lg">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-center">米斯特 門市考核查詢系統</h1>
        </div>
      </header>

      {/* Navigation */}
      <nav className="bg-card border-b border-border">
        <div className="container mx-auto px-4">
          <div className="flex space-x-1">
            {[
              { id: 'summary', label: '門店 考核總表' },
              { id: 'efficiency', label: '人效分析' },
              { id: 'detail', label: '考核明細' }
            ].map((tab) => (
              <Button
                key={tab.id}
                variant={activeTab === tab.id ? 'default' : 'ghost'}
                className="rounded-none border-b-2 border-transparent data-[state=active]:border-primary"
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </Button>
            ))}
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-6">
        {/* Action Bar */}
        <div className="flex justify-between items-center mb-6">
          <div className="flex space-x-2">
            <Button variant="outline" size="sm">
              <Search className="w-4 h-4 mr-2" />
              搜尋
            </Button>
            <Button variant="outline" size="sm">
              <Filter className="w-4 h-4 mr-2" />
              篩選
            </Button>
          </div>
          <Button variant="outline" size="sm">
            <Download className="w-4 h-4 mr-2" />
            匯出
          </Button>
        </div>

        {/* Content Sections */}
        {activeTab === 'summary' && (
          <div>
            {renderTable(filteredData.summary, '門店 考核總表', filteredData.summary.length)}
          </div>
        )}

        {activeTab === 'efficiency' && (
          <div>
            {renderTable(filteredData.efficiency, '人效分析', filteredData.efficiency.length, ['達成', '績效'])}
          </div>
        )}

        {activeTab === 'detail' && (
          <div>
            <div className="mb-4">
              <Badge variant="secondary" className="mb-2">店主管 考核明細</Badge>
            </div>
            {renderTable(filteredData.manager_detail, '店主管 考核明細', filteredData.manager_detail.length)}
            
            <div className="mb-4 mt-8">
              <Badge variant="secondary" className="mb-2">店員 考核明細</Badge>
            </div>
            {renderTable(filteredData.staff_detail, '店員 考核明細', filteredData.staff_detail.length)}
          </div>
        )}

        {/* Footer Note */}
        <div className="mt-8 p-4 bg-muted rounded-lg">
          <p className="text-sm text-muted-foreground">
            ※如對分數有疑問，請洽直屬區主管/品牌經理說明。
          </p>
          <p className="text-xs text-muted-foreground mt-2">
            資料來源: 2025.06門市-考核總表.xlsx
          </p>
        </div>
      </main>
    </div>
  )
}

export default App

