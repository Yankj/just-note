/**
 * E2E 测试 - 认证设置
 * 创建全局认证状态，供其他测试使用
 */
import { test as setup, expect } from '@playwright/test';

const authFile = 'playwright/.auth/user.json';

setup('authenticate as user', async ({ page }) => {
  // 前往登录页面
  await page.goto('/login');
  
  // 执行登录流程
  await page.getByPlaceholder('用户名').fill('testuser');
  await page.getByPlaceholder('密码').fill('TestPass123!');
  await page.getByRole('button', { name: '登录' }).click();
  
  // 等待登录成功（跳转到首页或仪表盘）
  await expect(page).toHaveURL(/.*dashboard.*/);
  
  // 保存认证状态
  await page.context().storageState({ path: authFile });
});

setup('register new user', async ({ page }) => {
  // 前往注册页面
  await page.goto('/register');
  
  // 填写注册表单
  await page.getByPlaceholder('用户名').fill('testuser');
  await page.getByPlaceholder('邮箱').fill('test@example.com');
  await page.getByPlaceholder('密码').fill('TestPass123!');
  await page.getByPlaceholder('确认密码').fill('TestPass123!');
  await page.getByRole('button', { name: '注册' }).click();
  
  // 等待注册成功
  await expect(page).toHaveURL(/.*login.*/);
});
