-- =====================================================
-- Supabase Storage Configuration
-- =====================================================

-- Create storage bucket for product images
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'products',
    'products',
    true,
    5242880, -- 5MB
    ARRAY['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif']
);

-- =====================================================
-- Storage Policies for 'products' bucket
-- =====================================================

-- Allow public read access to published product images
CREATE POLICY "Public read access for published products"
ON storage.objects FOR SELECT
USING (
    bucket_id = 'products' AND
    (
        -- Public access to all images (we control visibility via product status in app)
        true
    )
);

-- Allow authenticated admins to upload images
CREATE POLICY "Admins can upload product images"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'products' AND
    auth.role() = 'authenticated' AND
    EXISTS (
        SELECT 1 FROM app_users
        WHERE app_users.id = auth.uid()
        AND app_users.role = 'admin'
    )
);

-- Allow authenticated admins to update images
CREATE POLICY "Admins can update product images"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'products' AND
    auth.role() = 'authenticated' AND
    EXISTS (
        SELECT 1 FROM app_users
        WHERE app_users.id = auth.uid()
        AND app_users.role = 'admin'
    )
);

-- Allow authenticated admins to delete images
CREATE POLICY "Admins can delete product images"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'products' AND
    auth.role() = 'authenticated' AND
    EXISTS (
        SELECT 1 FROM app_users
        WHERE app_users.id = auth.uid()
        AND app_users.role = 'admin'
    )
);

-- =====================================================
-- Additional buckets (optional, for future use)
-- =====================================================

-- Bucket for user avatars
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'avatars',
    'avatars',
    true,
    2097152, -- 2MB
    ARRAY['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
);

-- Users can upload their own avatar
CREATE POLICY "Users can upload own avatar"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'avatars' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

-- Users can update their own avatar
CREATE POLICY "Users can update own avatar"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'avatars' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

-- Users can delete their own avatar
CREATE POLICY "Users can delete own avatar"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'avatars' AND
    auth.role() = 'authenticated' AND
    (storage.foldername(name))[1] = auth.uid()::text
);

-- Public read access to avatars
CREATE POLICY "Public read access to avatars"
ON storage.objects FOR SELECT
USING (bucket_id = 'avatars');

-- =====================================================
-- Bucket for banners (admin only)
-- =====================================================

INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'banners',
    'banners',
    true,
    10485760, -- 10MB
    ARRAY['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
);

-- Only admins can manage banners
CREATE POLICY "Admins can upload banners"
ON storage.objects FOR INSERT
WITH CHECK (
    bucket_id = 'banners' AND
    auth.role() = 'authenticated' AND
    EXISTS (
        SELECT 1 FROM app_users
        WHERE app_users.id = auth.uid()
        AND app_users.role = 'admin'
    )
);

CREATE POLICY "Admins can update banners"
ON storage.objects FOR UPDATE
USING (
    bucket_id = 'banners' AND
    auth.role() = 'authenticated' AND
    EXISTS (
        SELECT 1 FROM app_users
        WHERE app_users.id = auth.uid()
        AND app_users.role = 'admin'
    )
);

CREATE POLICY "Admins can delete banners"
ON storage.objects FOR DELETE
USING (
    bucket_id = 'banners' AND
    auth.role() = 'authenticated' AND
    EXISTS (
        SELECT 1 FROM app_users
        WHERE app_users.id = auth.uid()
        AND app_users.role = 'admin'
    )
);

-- Public read access to banners
CREATE POLICY "Public read access to banners"
ON storage.objects FOR SELECT
USING (bucket_id = 'banners');
